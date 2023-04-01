import altair as alt
import pandas as pd


def create_chart(df: pd.DataFrame) -> alt.Chart:
    chart = (
        alt.Chart(df.sort_values(["Stück", "ID"]))  # type: ignore
        .mark_bar(strokeOpacity=1, strokeWidth=2, stroke="white")  # type: ignore
        .encode(
            y=alt.Y("Stück:N", scale=alt.Scale(zero=False)),  # type: ignore
            x=alt.X("Länge:Q", scale=alt.Scale(zero=False)),  # type: ignore
            detail="ID:N",
            color=alt.condition(
                alt.datum.Typ == "Waste",
                alt.value("#fa5f0f"),
                alt.value("#9f9896"),
            ),
        )
        .properties(width=600, height=300)
    )
    return chart
