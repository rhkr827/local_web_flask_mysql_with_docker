# For application discovery by the 'flask' command.
from flask import Flask, render_template
import my_modules.connect as conn

# Import the Flask class
app = Flask(__name__)    #


@app.route("/")
def home():
    data = conn.run()
    return render_template("home.html")


@app.route("/history/")
def layout():
    return render_template("history.html")


@app.route("/summary/")
def about():
    return render_template("summary.html")


if __name__ == '__main__':
    app.run(debug=True)
