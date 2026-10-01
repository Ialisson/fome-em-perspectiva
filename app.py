from pathlib import Path

import streamlit as st

from fome_brasil.charts import national_trend_chart, regional_comparison_chart
from fome_brasil.data import load_data

DATA_PATH = Path(__file__).parent / "data" / "inseguranca_alimentar.csv"

st.set_page_config(page_title="Fome em perspectiva | Brasil", page_icon="🍽️", layout="wide")
st.markdown("""<style>
.block-container{max-width:1220px;padding-top:2rem;padding-bottom:4rem}
h1,h2,h3{letter-spacing:-.035em}
[data-testid="stMetric"]{background:rgba(255,255,255,.52);border:1px solid #ded9cf;padding:1rem;border-radius:.35rem}
.kicker{color:#c94d2c;font-size:.76rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.deck{font-family:Georgia,serif;font-size:1.16rem;line-height:1.55;max-width:850px;color:#4e4d47}
</style><div class="kicker">Caderno de dados · Brasil</div>""", unsafe_allow_html=True)
st.title("A fome tem história")
st.markdown('<p class="deck">Uma leitura interativa da insegurança alimentar grave: o que mudou, onde a desigualdade permanece e o que os dados não permitem concluir.</p>', unsafe_allow_html=True)

try:
    data = load_data(DATA_PATH)
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Não foi possível carregar a base: {exc}")
    st.stop()

national = data[(data["territory_type"] == "Brasil") & data["value"].notna()].copy()
regional = data[(data["territory_type"] == "Grande Região") & data["value"].notna()].copy()

with st.sidebar:
    st.header("Explore os dados")
    view = st.radio("Escolha uma visualização", ["Evolução no Brasil", "Diferenças entre regiões", "Base de dados"])
    st.divider()
    st.subheader("Sobre esta medida")
    st.write("A EBIA classifica domicílios segundo a experiência de acesso a alimentos. A taxa mostrada é domiciliar, não uma contagem de pessoas.")
    with st.expander("Por que há uma lacuna?"):
        st.write("O IBGE não aplicou a EBIA em pesquisa domiciliar oficial entre a POF 2017–2018 e a PNAD Contínua 2023. Os anos ausentes não foram estimados.")
    with st.expander("As pesquisas são iguais?"):
        st.write("PNAD, POF e PNAD Contínua usam a EBIA, mas diferem no desenho amostral e no período de coleta. Os inquéritos VIGISAN têm desenho próprio e não foram combinados com a série do IBGE.")

if view == "Evolução no Brasil":
    st.header("Como a prevalência mudou")
    st.write("A proporção publicada caiu de 6,9% em 2004 para 3,2% em 2024. Cada ponto corresponde a um levantamento; a lacuna entre 2018 e 2023 permanece visível.")
    latest = national.loc[national["year"] == national["year"].max()].iloc[0]
    previous = national.loc[national["year"] == 2023].iloc[0]
    first = national.loc[national["year"] == national["year"].min()].iloc[0]
    cols = st.columns(3)
    cols[0].metric("Brasil · 2024", f"{latest['value']:.1f}%".replace(".", ","))
    cols[1].metric("Brasil · 2023", f"{previous['value']:.1f}%".replace(".", ","))
    cols[2].metric("Brasil · 2004", f"{first['value']:.1f}%".replace(".", ","))
    st.plotly_chart(national_trend_chart(national), use_container_width=True)
    st.info("Em 2024, o resultado igualou o menor percentual desta série, observado também em 2013. Uma série descritiva não identifica, por si só, as causas da mudança.")
    with st.expander("Ver valores e fontes"):
        show = national[["period", "value", "survey", "source"]].copy()
        show.columns = ["Período", "Domicílios (%)", "Pesquisa", "Fonte"]
        st.dataframe(show, hide_index=True, use_container_width=True, column_config={"Fonte": st.column_config.LinkColumn("Fonte", display_text="Abrir fonte")})

elif view == "Diferenças entre regiões":
    st.header("O país não vive uma única curva")
    st.write("Compare a prevalência de domicílios em insegurança alimentar grave entre as Grandes Regiões. Todos os pontos vêm da PNAD Contínua 2024.")
    available = regional.sort_values("value", ascending=False)["territory"].tolist()
    chosen = st.multiselect("Regiões para comparar", available, default=available)
    selected = regional[regional["territory"].isin(chosen)]
    if selected.empty:
        st.warning("Selecione ao menos uma região.")
    else:
        st.plotly_chart(regional_comparison_chart(selected), use_container_width=True)
        high, low = selected.loc[selected["value"].idxmax()], selected.loc[selected["value"].idxmin()]
        cols = st.columns(2)
        cols[0].metric("Maior entre as selecionadas", f"{high['territory']}: {high['value']:.1f}%".replace(".", ","))
        cols[1].metric("Menor entre as selecionadas", f"{low['territory']}: {low['value']:.1f}%".replace(".", ","))
    st.caption("A escala começa em zero. Valores arredondados a uma casa decimal.")

else:
    st.header("Consulte e baixe a base")
    st.write("Filtre os registros, abra a fonte original de cada estimativa e baixe a seleção em CSV.")
    territories = ["Todos"] + sorted(data["territory"].dropna().unique().tolist())
    territory = st.selectbox("Filtrar território", territories)
    filtered = data if territory == "Todos" else data[data["territory"] == territory]
    st.dataframe(
        filtered[["period", "territory", "value", "survey", "source", "notes"]],
        hide_index=True, use_container_width=True,
        column_config={
            "period": st.column_config.TextColumn("Período"),
            "territory": st.column_config.TextColumn("Território"),
            "value": st.column_config.NumberColumn("Domicílios (%)", format="%.1f%%"),
            "survey": st.column_config.TextColumn("Pesquisa"),
            "source": st.column_config.LinkColumn("Fonte", display_text="Abrir fonte"),
            "notes": st.column_config.TextColumn("Notas"),
        },
    )
    st.download_button("Baixar seleção em CSV", data=filtered.to_csv(index=False).encode("utf-8-sig"), file_name="inseguranca_alimentar_brasil.csv", mime="text/csv")

st.divider()
st.subheader("Fontes e método")
st.markdown(
    "Classificação pela [Escala Brasileira de Insegurança Alimentar (EBIA)](https://www.ibge.gov.br/estatisticas/sociais/saude/17270-pnad-continua.html). "
    "Consulte [IBGE 2017–2018](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/28896-pof-2017-2018-proporcao-de-domicilios-com-seguranca-alimentar-fica-abaixo-do-resultado-de-2004), "
    "[PNAD Contínua 2023](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102084.pdf) e "
    "[PNAD Contínua 2024](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102212_informativo.pdf)."
)
st.caption("Projeto de portfólio · Jornalismo de dados · Fontes primárias do IBGE")
