from flask import Flask, render_template
from Inzidenzraumcreator import generate_inzidenzraum_with_points, generate_inzidenzraum_with_lines
from DominationFinder import find_domination

app = Flask(__name__)

@app.route('/points/<int:points>')
def points(points):
    df = generate_inzidenzraum_with_points(points)
    # domination = find_domination(df)
    domination = 'no domination'
    return render_template("analysis.html", data=df.to_html(), domination=domination)

@app.route('/lines/<int:lines>')
def lines(lines):
    df = generate_inzidenzraum_with_lines(lines)
    # domination = find_domination(df)
    domination = 'no domination'
    return render_template("analysis.html", data=df.to_html(), domination=domination)

if __name__ == "__main__":
    app.run()