from flask import Flask, render_template, url_for
import parser


app = Flask(__name__)

@app.route('/')
def index():
    date_weather = parser.get_data()
    return render_template("index.html", days = date_weather, color_by_sign=parser.color_by_sign)


if __name__ == "__main__":
    app.run(debug=True)
