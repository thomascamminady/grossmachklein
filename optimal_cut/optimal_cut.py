from itertools import combinations


def find_best_cuts(long_stick: float, smaller_sticks: list[float]) -> list[float]:
    best_cuts = []
    best_waste = long_stick

    for i in range(1, len(smaller_sticks) + 1):
        for comb in combinations(smaller_sticks, i):
            waste = long_stick - sum(comb)
            if 0 <= waste < best_waste:
                best_waste = waste
                best_cuts = comb

    return list(best_cuts)


def compute_optimal_cuts(
    long_stick: float, smaller_sticks: list[float]
) -> tuple[list[list[float]], float]:
    result = []
    waste = 0
    remaining_pieces = smaller_sticks.copy()

    while sum(remaining_pieces) > 0:
        optimal_cuts_for_stick = find_best_cuts(long_stick, remaining_pieces)
        result.append(optimal_cuts_for_stick)
        waste += long_stick - sum(optimal_cuts_for_stick)

        for cut in optimal_cuts_for_stick:
            remaining_pieces.remove(cut)

    return result, waste
