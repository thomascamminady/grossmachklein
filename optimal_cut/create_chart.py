import altair as alt
import pandas as pd


def create_chart(df: pd.DataFrame) -> alt.Chart:
    chart = (
        alt.Chart(df.sort_values(["Stück", "ID"]))
        .mark_bar(strokeOpacity=1, strokeWidth=2, stroke="white")
        .encode(
            y=alt.Y("Stück:N", scale=alt.Scale(zero=False)),
            x=alt.X("Länge:Q", scale=alt.Scale(zero=False)),
            detail="ID:N",
            color=alt.condition(
                alt.datum.Typ == "Waste",
                alt.value("#de2d26"),
                alt.value("#636363"),
            ),
        )
        .properties(width=600, height=400)
    )
    return chart
