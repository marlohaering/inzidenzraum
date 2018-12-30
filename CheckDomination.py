from typing import Set
import pandas as pd


def check_domination(i: pd.DataFrame, S: Set, full_domination) -> bool:
    current_domination = set()

    for e in S:
        current_domination.add(e)
        if isinstance(e, int):
            # ist ein Punkt bzw. Zeile
            marked_lines = i.columns[i.loc[e] == 1]
            current_domination.update(marked_lines)
        else:
            # ist eine Gerade bzw. Spalte
            markes_points = i.index[i[e] == 1]
            current_domination.update(markes_points)

    return current_domination == full_domination


def check_domination2(i: pd.DataFrame, S: Set, full_domination) -> bool:
    current_domination = set(full_domination)

    for e in S:
        current_domination.discard(e)
        if isinstance(e, int):
            # ist ein Punkt bzw. Zeile
            marked_lines = i.columns[i.loc[e] == 1].tolist()
            current_domination -= set(marked_lines)
        else:
            # ist eine Gerade bzw. Spalte
            markes_points = i.index[i[e] == 1].tolist()
            current_domination -= set(markes_points)

    return not current_domination
