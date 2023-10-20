import pandas as pd


def to_dataframe(
    piece_id: int,
    length: float,
    type: str,
    cut_id: int,
) -> pd.DataFrame:
    return pd.DataFrame(
        [{"Stück": piece_id, "Länge": length, "Typ": type, "ID": cut_id}]
    )


def create_dataframe(
    long_stick: float, optimal_cuts: list[list[float]]
) -> pd.DataFrame:
    df_list = []
    for piece_id, cuts_for_piece in enumerate(optimal_cuts):
        cuts_for_piece.sort()
        for cut_id, cut_length in enumerate(cuts_for_piece):
            df_list.append(
                to_dataframe(
                    piece_id + 1,
                    cut_length,
                    "Schnitt",
                    cut_id,
                )
            )

        waste = long_stick - sum(cuts_for_piece)
        df_list.append(
            to_dataframe(
                piece_id + 1,
                waste,
                "Waste",
                len(cuts_for_piece),
            )
        )
    return pd.concat(df_list)
