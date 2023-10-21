from baseconfig import app
from flask import render_template
import numpy as np
import cv2


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/lossy-compression", methods=["GET"])
def lossy_compression():
    # Task 1


    return render_template("index.html")

@app.route("/lossy-compression-2", methods=["GET"])
def lossy_compression_2():
    # Task 2
    
    return render_template("index.html")

@app.route("/wavelet-mra", methods=["GET"])
def wavelet_mra():
    # Task 3
    
    return render_template("index.html")

@app.route("/wavelet_transform", methods=["GET"])
def wavelet_transform():
    # Task 4
    
    return render_template("index.html")

@app.route("/harnverhalt", methods=["GET"])
def harnverhalt():
    # Task 5

    return render_template("harnverhalt.html")

@app.route("/cmp", methods=["GET"])
def cmp():
    # Task 6

    return render_template("cmp.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
