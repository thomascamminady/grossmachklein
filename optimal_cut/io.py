import streamlit as st

from optimal_cut import logger


def parse_input(input_text: str) -> list[float]:
    small_pieces = []
    for row in input_text.strip().split("\n"):
        for s in row.strip().split(","):
            try:
                small_pieces.append(float(s))
            except Exception as e:
                warning = f"Das hier scheint nicht korrekt zu sein: {s}"
                st.warning(warning)
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
                f"Wir können kein {small_stick} Stück "
                + "aus einem {long_stick} Stück schneiden. "
                + "Das Stück wird ignoriert."
            )
        else:
            valid_small_sticks.append(small_stick)
    return valid_small_sticks
