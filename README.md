# Fome em perspectiva

> Aplicação interativa de jornalismo de dados sobre insegurança alimentar grave no Brasil.

**Pergunta editorial:** como a prevalência mudou nos levantamentos nacionais e como varia entre as regiões brasileiras?

**O que os dados mostram:** o percentual domiciliar publicado foi de 6,9% em 2004 e 3,2% em 2024. A série não é anual; há uma lacuna de coleta oficial entre 2018 e 2023. Em 2024, a prevalência variou de 6,3% no Norte a 1,7% no Sul.

O projeto não atribui mudanças a presidentes ou políticas específicas: uma série descritiva não demonstra causalidade.

## Experiência interativa

- **Evolução no Brasil:** explore os pontos do gráfico e veja a lacuna sem coleta do IBGE.
- **Diferenças entre regiões:** filtre as Grandes Regiões na comparação de 2024.
- **Base de dados:** consulte registros, abra as fontes e baixe a seleção em CSV.
- **Leitura guiada:** veja explicações de método junto às visualizações.

## Tecnologias e decisões

- **Python + Streamlit:** interface, navegação e controles interativos.
- **pandas:** leitura, tipagem e validação da base local.
- **Plotly:** gráficos interativos; valores ausentes não são conectados.
- **CSV local:** cada estimativa retém período, pesquisa, fonte e nota.
- **GitHub Actions + Ruff:** checagem de código e compilação em push e pull request.

## Estrutura

    .
    ├── .github/workflows/python-check.yml
    ├── .streamlit/config.toml
    ├── app.py
    ├── data/
    │   ├── README.md
    │   └── inseguranca_alimentar.csv
    ├── fome_brasil/
    │   ├── __init__.py
    │   ├── charts.py
    │   └── data.py
    ├── .gitignore
    ├── .python-version
    ├── pyproject.toml
    ├── requirements-dev.txt
    └── requirements.txt

## Executar localmente

Requer Python 3.10 ou superior; recomenda-se Python 3.12.

### Windows PowerShell

    py -3.12 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

### macOS ou Linux

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

Para desenvolvimento, instale também Ruff: python -m pip install -r requirements-dev.txt.

## Publicar com GitHub e Streamlit Community Cloud

1. Envie os arquivos a um repositório GitHub na branch main.
2. Acesse [Streamlit Community Cloud](https://share.streamlit.io/) e conecte sua conta GitHub.
3. Selecione o repositório, a branch e app.py como arquivo principal.
4. Publique. A plataforma instala requirements.txt.

O app não usa chaves de API nem credenciais.

## Dados, fontes e limites

O indicador é o percentual de **domicílios** classificados com insegurança alimentar grave pela Escala Brasileira de Insegurança Alimentar (EBIA). Não equivale à contagem de pessoas afetadas.

| Período | Percentual domiciliar | Levantamento |
|---|---:|---|
| 2004 | 6,9% | PNAD |
| 2009 | 5,0% | PNAD |
| 2013 | 3,2% | PNAD |
| 2017–2018 | 4,6% | POF |
| 2023 | 4,1% | PNAD Contínua |
| 2024 | 3,2% | PNAD Contínua |

PNAD, POF e PNAD Contínua usam a EBIA, mas têm desenhos amostrais e períodos de coleta distintos. Os pontos são resultados publicados, não uma série anual homogênea. O IBGE não aplicou a EBIA em pesquisa domiciliar oficial entre a POF 2017–2018 e a PNAD Contínua 2023. Os anos ausentes não foram interpolados. Os inquéritos da Rede PENSSAN têm desenho próprio e não foram misturados à série do IBGE.

A comparação regional usa somente as Grandes Regiões de 2024, dentro do mesmo levantamento. Consulte o [dicionário de dados](data/README.md).

### Fontes primárias

- [IBGE — PNAD 2004/2009](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/13935-asi-inseguranca-alimentar-diminui-mas-ainda-atinge-302-dos-domicilios-brasileiros)
- [IBGE — PNAD 2013](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/14735-asi-pnad-inseguranca-alimentar-nos-domicilios-cai-de-302-em-2009-para-226-em-2013)
- [IBGE — POF 2017–2018](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/28896-pof-2017-2018-proporcao-de-domicilios-com-seguranca-alimentar-fica-abaixo-do-resultado-de-2004)
- [IBGE — PNAD Contínua 2023](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102084.pdf)
- [IBGE — PNAD Contínua 2024](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102212_informativo.pdf)

## Próximas melhorias

1. Adicionar comparação por estado junto com notas de precisão.
2. Criar visões próprias para raça/cor e renda, respeitando denominadores e universos.
3. Acrescentar testes para validar atualizações futuras da base.
