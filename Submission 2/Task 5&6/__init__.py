from baseconfig import app
from flask import render_template
import numpy as np
import cv2

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
