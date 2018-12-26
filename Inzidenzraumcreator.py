import numpy as np
import pandas as pd
import itertools as it
from random import choice, shuffle
import signal
import itertools


def check_inzidenzraum(m: np.array):
    if type(m) is not np.ndarray:
        return False

    rows, columns = m.shape

    # Bedingung 1:
    # In jeder Spalte mindestens zwei einsen
    for j in range(columns):
        if m[:, j].sum() < 2:
            return False

    # Bedingung 2:
    row_combinations = list(it.permutations(range(rows), 2))
    for i, j in row_combinations:
        found_1_1 = 0
        for column in range(columns):
            if m[i, column] == 1 and m[j, column] == 1:
                found_1_1 += 1
        if found_1_1 < 1 or found_1_1 > 1:
            return False

    return True


def load_matrix_from_file():
    f = open('graph.txt', 'r')
    l = [[int(num) for num in line.split(' ')] for line in f]
    return np.array(l)


def generate_non_zero_row(size):
    while True:
        next_row = np.random.randint(2, size=size)
        if next_row.sum() > 0:
            break
    return next_row


def check_previous_columns(m: np.array, column: np.array)->bool:
    rows, columns = m.shape
    for j in range(columns):
        found_1_1 = 0
        current_column = m[:, j]
        for row in range(rows):
            if m[row, j] == 1 and column[row] == 1:
                found_1_1 += 1
            if found_1_1 > 1:
                return False
        if found_1_1 > 1:
            return False
    return True


def check_previous_rows(m, row):
    rows, columns = m.shape
    for i in range(rows):
        found_1_1 = 0
        current_row = m[i, :]
        for column in range(columns):
            if m[i, column] == 1 and row[column] == 1:
                found_1_1 += 1
            if found_1_1 > 1:
                return False
        if found_1_1 != 1:
            return False
    return True


def handler(signum, frame):
    raise Exception("end of timeout")


def generate_matrix_point_by_point(size: int) -> np.ndarray:
    matrix = np.empty((size, size), dtype=np.int8)
    first_row = generate_non_zero_row(size)
    matrix[0] = first_row
    for row in range(1, size):
        previous_row = matrix[row-1, :]
        one_indexes = list(previous_row.nonzero()[0])
        shuffle(one_indexes)
        random_one_index = one_indexes.pop()

        try:
            signal.signal(signal.SIGALRM, handler)
            signal.setitimer(signal.ITIMER_REAL, 0.1)
            while True:
                # zufällige zeile mit mindestens einer 1
                next_row = generate_non_zero_row(size)

                if check_previous_rows(matrix[:row, :], next_row):
                    break
        except Exception as e:
            return matrix[:row, :]
        matrix[row, :] = next_row

    return matrix


def generate_new_line_with_at_least_two_points(size):
    while True:
        line = generate_non_zero_row(size)
        if line.sum() >= 2:
            return line


def generate_matrix_line_by_line(size: int) -> np.array:
    matrix = np.empty((size, size*10), dtype=np.int8)
    first_column = generate_new_line_with_at_least_two_points(size)
    matrix[:, 0] = first_column

    if check_inzidenzraum(matrix[:, :1]):
        return matrix[:, :1]

    for column in range(1, size*10):  # todo: mal 10 willkürlich

        while True:
            next_column = generate_new_line_with_at_least_two_points(size)
            if check_previous_columns(matrix[:, :column], next_column):
                break

        matrix[:, column] = next_column

        if check_inzidenzraum(matrix[:, :column+1]):
            return matrix[:, :column+1]

    return matrix


def generate_column_labels():

    number_letters = 1
    chars = "abcdefghijklmnopqrstuvwxyz"
    while True:
        for item in itertools.product(chars, repeat=number_letters):
            yield ''.join(item)
        number_letters += 1


def create_inzidenzraum_df(matrix: np.array):
    column_labels = itertools.islice(generate_column_labels(), matrix.shape[1])

    df = pd.DataFrame(matrix, columns=column_labels)

    df.index = np.arange(1, len(df) + 1)  # start rows with one
    df['#lines through point'] = df.sum(axis=1)
    df.loc['#points on line'] = df.sum()
    df.at['#points on line', '#lines through point'] = 0

    return df


def generate_inzidenzraum_by_point(number_lines: int) -> pd.DataFrame:

    matrix = None
    while not check_inzidenzraum(matrix):
        matrix = generate_matrix_point_by_point(number_lines)

    signal.alarm(0)
    return create_inzidenzraum_df(matrix)


def generate_inzidenzraum_by_line(number_points: int) -> pd.DataFrame:
    matrix = None
    while not check_inzidenzraum(matrix):
        matrix = generate_matrix_line_by_line(number_points)

    return create_inzidenzraum_df(matrix)


if __name__ == "__main__":
    print(generate_inzidenzraum_by_point(6))
