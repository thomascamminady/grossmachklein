import streamlit as st

from optimal_cut import logger
from optimal_cut.create_chart import create_chart
from optimal_cut.io import parse_input, remove_sticks_that_are_too_large
from optimal_cut.optimal_cut import compute_optimal_cuts
from optimal_cut.to_dataframe import create_dataframe

if __name__ == "__main__":
    st.image("assets/logo.jpg", width=400)
    st.title("Aus groß mach klein!")
    small_sticks_strings = st.text_area(
        "Kleine Maße kommen hier rein. Angaben in Zentimetern. Z.B.: 100,200,150",
        height=100,
    )
    col1, col2 = st.columns(2)
    with col1:
        long_stick = st.number_input("Große Länge in Zentimetern.", value=598)
    with col2:
        buffer = st.number_input(
            "Puffer pro Schnitt in Zentimetern.",
            value=0.0,
            min_value=0.0,
            max_value=1.0,
            step=1e-1,
            format="%.1f",
        )
    if st.button("Plan erstellen"):
        small_sticks = parse_input(small_sticks_strings)

        logger.info(small_sticks)
        small_sticks = remove_sticks_that_are_too_large(long_stick, small_sticks)
        optimal_cuts, waste = compute_optimal_cuts(
            long_stick, smaller_sticks=small_sticks, buffer=buffer
        )

        st.markdown("## Überblick")
        st.markdown(f"Verschnitt in Orange. Insgesamt: {waste} cm")
        df = create_dataframe(long_stick, optimal_cuts)
        st.altair_chart(create_chart(df))

        st.markdown("## So kannst du schneiden")
        for i, plan in enumerate(optimal_cuts):
            st.write(
                f"- Großes Stück {i+1}    (Verschnitt: {long_stick-sum(plan)} cm)"
                + "\n   - "
                + "\n  - ".join([f"{x} cm" for x in plan])
            )
        logger.info("Magic:")
        logger.info(small_sticks)
        logger.info(optimal_cuts)
