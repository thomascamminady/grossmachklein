import altair as alt
import pandas as pd
import streamlit as st

from optimal_cut import logger
from optimal_cut.io import parse_input, remove_sticks_that_are_too_large
from optimal_cut.optimal_cut import compute_optimal_cuts

if __name__ == "__main__":
    st.title("Aus groß mach klein!")
    small_sticks_strings = st.text_area(
        "Kleine Maße kommen hier rein. Angaben in Zentimetern. Z.B.: 100,200,150",
        height=100,
    )
    long_stick = st.number_input("Große Länge in Zentimetern.", value=600)
    buffer = st.number_input("Puffer pro Schnitt in Zentimetern.", value=0)
    if st.button("Click here for magic!"):
        small_sticks = parse_input(small_sticks_strings)

        logger.info(small_sticks)
        small_sticks = remove_sticks_that_are_too_large(long_stick, small_sticks)
        st.markdown("## So kannst du schneiden:")
        optimal_cuts, waste = compute_optimal_cuts(
            long_stick, smaller_sticks=small_sticks, buffer=buffer
        )

        dflist = []
        for i, plan in enumerate(optimal_cuts):
            plan.sort()
            for j, x in enumerate(plan):
                dflist.append(
                    pd.DataFrame(
                        [
                            {
                                "Stück": i + 1,
                                "Länge": x,
                                "Typ": "Schnitt",
                                "ID": j,
                                "even": j % 2,
                            }
                        ]
                    )
                )

            dflist.append(
                pd.DataFrame(
                    [
                        {
                            "Stück": i + 1,
                            "Länge": long_stick - sum(plan),
                            "Typ": "Waste",
                            "ID": len(plan),
                            "even": 2,
                        }
                    ]
                )
            )

            st.write(
                f"- Großes Stück {i+1}    (Verschnitt: {long_stick-sum(plan)}cm)"
                + "\n   - "
                + "\n  - ".join([f"{x} cm" for x in plan])
            )

        st.markdown("## Grafik (rot ist Verschnitt)")

        df = pd.concat(dflist)
        # legend_selection = alt.selection_point(fields=["SHAPE_OR_COLOR"], bind="legend")
        chart = (
            alt.Chart(df.sort_values(["Stück", "ID"]))
            .mark_bar(strokeOpacity=1, strokeWidth=2, stroke="white")
            # .mark_line(clip=True)
            .encode(
                y=alt.Y("Stück:N", scale=alt.Scale(zero=False)),
                x=alt.X("Länge:Q", scale=alt.Scale(zero=False)),
                detail="ID:N",
                color=alt.condition(
                    alt.datum.Typ == "Waste", alt.value("red"), alt.value("black")
                ),
            )
            .properties(width=600, height=400)
        )

        st.altair_chart(chart)
        logger.info("Magic:")
        logger.info(small_sticks)
        logger.info(optimal_cuts)
