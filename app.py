import streamlit as st
from optimal_cut import logger
from optimal_cut.optimal_cut import compute_optimal_cuts


def parse_input(input_text: str) -> list[float]:
    small_pieces = []
    for row in input_text.strip().split("\n"):
        for s in row.strip().split(","):
            try:
                small_pieces.append(float(s))
            except Exception as e:
                st.warning(f"Das hier scheint keine korrekte Eingabe zu sein: {s}")
                logger.error(f"Parsing: {input_text}")
                logger.error(e)
    return small_pieces


def remove_sticks_that_are_too_large(
    long_stick: float, small_sticks: list[float]
) -> list[float]:
    valid_small_sticks = []
    for small_stick in small_sticks:
        if small_stick > long_stick:
            st.warning(
                f"Wir können kein {small_stick} Stück aus einem {long_stick} Stück schneiden. Das Stück wird ignoriert."
            )
        else:
            valid_small_sticks.append(small_stick)
    return valid_small_sticks


if __name__ == "__main__":
    st.title("Aus groß mach klein!")
    small_sticks_strings = st.text_area(
        "Kleine Maße kommen hier rein. Angaben in Zentimetern.", height=100
    )
    long_stick = st.number_input("Große Länge in Zentimetern.", value=600)
    if st.button("Click here for magic!"):
        small_sticks = parse_input(small_sticks_strings)
        small_sticks = remove_sticks_that_are_too_large(long_stick, small_sticks)
        st.markdown("## So kannst du schneiden:")
        optimal_cuts, waste = compute_optimal_cuts(
            long_stick, smaller_sticks=small_sticks
        )

        for i, plan in enumerate(optimal_cuts):
            st.write(
                f"- Großes Stück {i+1}    (Verschnitt: {long_stick-sum(plan)}cm)"
                + "\n   - "
                + "\n  - ".join([f"{x} cm" for x in plan])
            )
        logger.info("Magic:")
        logger.info(small_sticks)
        logger.info(optimal_cuts)
