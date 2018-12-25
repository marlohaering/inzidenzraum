from flask import Flask, render_template
from Inzidenzraumcreator import generate_inzidenzraum_by_line, generate_inzidenzraum_by_point

app = Flask(__name__)

@app.route('/points/<int:points>')
def points(points):
    df = generate_inzidenzraum_by_line(points)
    return render_template("analysis.html", data=df.to_html())

@app.route('/lines/<int:lines>')
def lines(lines):
    df = generate_inzidenzraum_by_point(lines)
    return render_template("analysis.html", data=df.to_html())

if __name__ == "__main__":
    app.run()