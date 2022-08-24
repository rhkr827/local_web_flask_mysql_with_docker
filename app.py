# For application discovery by the 'flask' command.
from flask import Flask, render_template
from modules import *

# Import the Flask class
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# global variables
jobhistory = None
jobsummary = None


@app.route("/")
def index():
    global jobhistory, jobsummary
    jobhistory, jobsummary = run()
    return render_template("index.html", history=jobhistory, summary=jobsummary)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
