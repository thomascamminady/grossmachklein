from more_itertools import distinct_combinations

# from itertools import combinations


def find_best_cuts(
    long_stick: float, smaller_sticks: list[float], buffer: float
) -> list[float]:
    best_cuts = []
    best_waste = long_stick

    for i in range(1, len(smaller_sticks) + 1):
        # for comb_set in set(combinations(smaller_sticks, i)):
        # Below line is the same as this, except it does not generate
        # the combinations and discards them afterwards.
        for comb_set in distinct_combinations(smaller_sticks, i):
            comb = list(comb_set)
            waste = long_stick - sum(comb) - buffer * (len(comb) - 1)
            if 0 <= waste < best_waste:
                best_waste = waste
                best_cuts = comb
                if best_waste == 0:
                    return list(best_cuts)

    return list(best_cuts)


def compute_optimal_cuts(
    long_stick: float, smaller_sticks: list[float], buffer: float
) -> tuple[list[list[float]], float]:
    result = []
    waste = 0.0
    sorted(smaller_sticks)
    remaining_pieces = smaller_sticks.copy()

    while len(remaining_pieces) > 0:
        optimal_cuts_for_stick = find_best_cuts(
            long_stick,
            remaining_pieces,
            buffer,
        )
        result.append(optimal_cuts_for_stick)
        waste += long_stick - sum(optimal_cuts_for_stick)

        for cut in optimal_cuts_for_stick:
            remaining_pieces.remove(cut)

    return result, waste
