"""Leitura e validação da base local."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"period", "year", "territory_type", "territory", "value", "survey", "source", "notes"}
KEY_COLUMNS = ["period", "territory_type", "territory"]


def load_data(path: Path) -> pd.DataFrame:
    """Carrega o CSV e explica erros comuns de estrutura ou conteúdo."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Colunas ausentes: {', '.join(sorted(missing))}")

    raw_values = frame["value"].copy()
    frame["value"] = pd.to_numeric(raw_values, errors="coerce")
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    if (raw_values.notna() & frame["value"].isna()).any():
        raise ValueError("A coluna value contém valores não numéricos.")
    if frame["year"].isna().any():
        raise ValueError("A coluna year precisa ter um ano válido em todas as linhas.")
    if not frame["value"].dropna().between(0, 100).all():
        raise ValueError("Os percentuais precisam estar entre 0 e 100.")
    if frame.duplicated(KEY_COLUMNS).any():
        raise ValueError("Há registros duplicados para o mesmo período e território.")
    published = frame["value"].notna()
    if frame.loc[published, ["survey", "source"]].isna().any(axis=None):
        raise ValueError("Toda estimativa publicada precisa informar pesquisa e fonte.")
    return frame.sort_values(["territory_type", "year", "territory"], na_position="last").reset_index(drop=True)
