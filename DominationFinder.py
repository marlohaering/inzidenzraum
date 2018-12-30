import pandas as pd
from typing import Set
import itertools
from Inzidenzraumcreator import generate_inzidenzraum_with_lines, generate_inzidenzraum_with_points, create_inzidenzraum_df, check_inzidenzraum
from tqdm import tqdm
import numpy as np
from scipy.special import binom
from CheckDomination import check_domination, check_domination2


def get_points_and_lines(i: pd.DataFrame, separate=False) -> Set:
    if not separate:
        full_domination = set()
        full_domination.update(i.index.tolist()[:-1]) # add all points
        full_domination.update(i.columns.tolist()[:-1]) # add all lines
        return full_domination
    else:
        points = set()
        lines = set()
        points.update(i.index.tolist()[:-1])
        lines.update(i.columns.tolist()[:-1])
        return points, lines


def get_number_combinations(number_elements, lower_bound, max_bound):
    combinations = 0
    for i in range(lower_bound, max_bound+1):
        combinations += binom(number_elements, i)
    return combinations

def get_all_combinations(lines_and_points, x):
    return itertools.combinations(lines_and_points, x), binom(len(lines_and_points), x)

def get_less_combinations(points, lines, x, lower_bound):
    for i in range(1,lower_bound+1):
        for line_combination in itertools.combinations(lines, i):
            number_points = x - len(line_combination)
            for point_combination in itertools.combinations(points, number_points):
                combination = line_combination+point_combination
                yield combination

def find_domination(i: pd.DataFrame):
    points, lines = get_points_and_lines(i, separate=True)
    lower_bound = min(i['#lines through point'].tolist()[:-1])
    max_bound = len(i.index.tolist()) - 1 - max(i.iloc[-1].tolist()) + 1
    print(i)
    print(f'bounds: ({lower_bound}, {max_bound})')
    full_domination = get_points_and_lines(i)
    for x in range(lower_bound, max_bound+1):
        domination_combinations = get_less_combinations(points, lines, x, lower_bound)
        iterator = tqdm(domination_combinations, total=None)
        for candidate in iterator:
            if check_domination(i, candidate, full_domination):
                print(f'found one minimal dominating set: {candidate}')
                iterator.close()
                return candidate


if __name__ == "__main__":
    # i = generate_inzidenzraum_with_points(6)
    # i.to_pickle('inzidenzraum.pkl')
    # i = pd.read_pickle('inzidenzraum.pkl')
    matrix = np.array([
        [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
        [0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1],
        [0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0],
        [0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,1]
    ])


    print(check_inzidenzraum(matrix))
    i = create_inzidenzraum_df(matrix)
    print(i)
    find_domination(i)


    # for i in get_less_combinations({1,2,3,4}, {'a', 'b', 'c', 'd'}, 4, 2):
    #     print (i)