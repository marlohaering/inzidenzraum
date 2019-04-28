from flask import Flask, render_template, request
from Inzidenzraumcreator import generate_inzidenzraum_with_points, generate_inzidenzraum_with_lines
from DominationFinder import find_domination
import numpy as np
from DominationSolver import createGraph, get_domination_set
import json

app = Flask(__name__)


@app.route('/points/<int:points>')
def points(points):
    df = generate_inzidenzraum_with_points(points)
    # domination = find_domination(df)
    domination = 'no domination'
    return render_template("analysis.html", data=df.to_html(), domination=domination)


def text_to_lines(text: str):
    numbers = []
    line_strings = text.split('\n')
    for line_string in line_strings:
        elements = line_string.split(',')
        elements = [int(e) for e in elements]
        numbers.append(elements)

    return np.array(numbers)


@app.route('/points', methods=['GET', 'POST'])
def points_with_lines():
    data = request.form.get('lines', False)
    if data:
        lines = text_to_lines(data)
        df = generate_inzidenzraum_with_points(None, lines)
    else:
        df = generate_inzidenzraum_with_points(5, None)
    # domination = find_domination(df)
    domination = 'no domination'
    return render_template("analysis.html", data=df.to_html(), domination=domination)


@app.route('/lines/<int:lines>')
def lines(lines):
    df = generate_inzidenzraum_with_lines(lines)
    # domination = find_domination(df)
    domination = 'no domination'
    return render_template("analysis.html", data=df.to_html(), domination=domination)


@app.route('/covering', methods=['POST'])
def covering():
    edges = request.form.get('edges', False)
    if edges:
        G = createGraph(edges)
        domination_set = get_domination_set(G)
        return str(domination_set) + f' number: {len(domination_set)}'
    return 'no edges given'


if __name__ == "__main__":
    app.run()
