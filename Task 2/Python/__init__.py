# Flask
from flask import render_template, url_for, redirect, flash

# App
from baseconfig import app


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")