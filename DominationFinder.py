import pandas as pd
from typing import Set
import itertools
from Inzidenzraumcreator import generate_inzidenzraum_with_lines, generate_inzidenzraum_with_points
from tqdm import tqdm
from scipy.special import binom


def get_points_and_lines(i: pd.DataFrame) -> Set:
    full_domination = set()
    full_domination.update(i.index.tolist()[:-1])
    full_domination.update(i.columns.tolist()[:-1])
    return full_domination

def get_number_combinations(number_elements, lower_bound, max_bound):
    combinations = 0
    for i in range(lower_bound, max_bound+1):
        combinations += binom(number_elements, i)
    return combinations


def find_domination(i: pd.DataFrame):
    full_domination = get_points_and_lines(i)
    lower_bound = min(i['#lines through point'].tolist()[:-1])
    max_bound = len(i.index.tolist()) - 1 - max(i.iloc[-1].tolist()) + 1
    print(i)
    print(f'bounds: ({lower_bound}, {max_bound})')
    for x in range(lower_bound, max_bound+1):
        iterator = tqdm(itertools.combinations(full_domination, x), total=binom(len(full_domination), x))
        for candidate in iterator:
            candidate_set = set(candidate)
            if check_domination(i, candidate_set):
                print(f'found one minimal dominating set: {candidate_set}')
                iterator.close()
                return candidate_set


def check_domination(i: pd.DataFrame, S: Set) -> bool:

    full_domination = get_points_and_lines(i)
    current_domination = set()

    for e in S:
        current_domination.add(e)
        if isinstance(e, int):
            # ist ein Punkt bzw. Zeile
            marked_lines = i.columns[i.loc[e] == 1].tolist()
            current_domination.update(marked_lines)
        else:
            # ist eine Gerade bzw. Spalte
            markes_points = i.index[i[e] == 1]
            current_domination.update(markes_points)

    return current_domination == full_domination


if __name__ == "__main__":
    i = generate_inzidenzraum_with_points(6)
    # i.to_pickle('inzidenzraum.pkl')
    # i = pd.read_pickle('inzidenzraum.pkl')
    find_domination(i)
