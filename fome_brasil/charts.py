"""Gráficos interativos do projeto."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PAPER, INK, ACCENT, GRID = "#f6f2e9", "#20221d", "#c94d2c", "#ded9cf"


def national_trend_chart(frame: pd.DataFrame) -> go.Figure:
    """Mostra a série e preserva o intervalo sem coleta oficial."""
    ordered = frame.sort_values("year").copy()
    gaps = pd.DataFrame([
        {"period": str(year), "year": year, "value": None,
         "survey": "Sem coleta EBIA do IBGE", "source": "", "territory": "Brasil"}
        for year in range(2019, 2023)
    ])
    chart_data = pd.concat([ordered, gaps], ignore_index=True).sort_values("year")
    chart_data["value_label"] = chart_data["value"].map(
        lambda value: f"{value:.1f}%".replace(".", ",") if pd.notna(value) else ""
    )
    fig = px.line(chart_data, x="year", y="value", markers=True,
                  custom_data=["period", "survey", "value_label"])
    fig.update_traces(
        line={"color": ACCENT, "width": 3},
        marker={"color": ACCENT, "size": 10, "line": {"color": PAPER, "width": 2}},
        connectgaps=False,
        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[2]} dos domicílios<br>%{customdata[1]}<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font={"family": "Arial, sans-serif", "color": INK},
        margin={"l": 16, "r": 20, "t": 20, "b": 20},
        xaxis={"title": "Ano/período da pesquisa", "tickmode": "array",
               "tickvals": ordered["year"], "ticktext": ordered["period"], "showgrid": False},
        yaxis={"title": "Domicílios em insegurança grave (%)", "range": [0, 8],
               "ticksuffix": "%", "gridcolor": GRID, "dtick": 2},
        hoverlabel={"bgcolor": INK, "font_color": "white"}, showlegend=False,
    )
    return fig


def regional_comparison_chart(frame: pd.DataFrame) -> go.Figure:
    """Compara regiões com barras horizontais e escala iniciada em zero."""
    ordered = frame.sort_values("value", ascending=True).copy()
    ordered["value_label"] = ordered["value"].map(lambda value: f"{value:.1f}%".replace(".", ","))
    fig = px.bar(ordered, x="value", y="territory", orientation="h",
                 text="value_label", custom_data=["survey", "value_label"],
                 color_discrete_sequence=[ACCENT])
    fig.update_traces(
        texttemplate="%{text}", textposition="outside", cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{customdata[1]} dos domicílios<br>%{customdata[0]}<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font={"family": "Arial, sans-serif", "color": INK},
        margin={"l": 18, "r": 55, "t": 18, "b": 20},
        xaxis={"title": "Domicílios em insegurança grave (%)", "range": [0, 8],
               "ticksuffix": "%", "gridcolor": GRID, "dtick": 2},
        yaxis={"title": "", "categoryorder": "array",
               "categoryarray": ordered["territory"].tolist()},
        hoverlabel={"bgcolor": INK, "font_color": "white"}, showlegend=False,
    )
    return fig
