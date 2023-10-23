from baseconfig import app
from wavelet import wavelet_transform_mra as wtmra
from wavelet import wavelet_transform as wt
from flask import render_template, request
from base64 import b64encode
from forms import waveletImageForm

# import numpy as np
# import cv2
# from io import BytesIO


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


@app.route("/wavelet-mra", methods=["POST", "GET"])
def wavelet_mra():
    form = waveletImageForm()
    input_image = None

    if form.submit.data and form.validate():
        image = request.files['image'].read()
        input_image = f"data:image/png;base64,{b64encode(image).decode('utf-8')}"
        mra = wtmra(image)        
 
        return render_template("wavelet-mra.html", form=form, input_image=input_image, mra = mra)
    return render_template("wavelet-mra.html", form=form, input_image = input_image)


@app.route("/wavelet_transform", methods=["POST", "GET"])
def wavelet_transform():
    form = waveletImageForm()
    input_image = None

    if form.submit.data and form.validate():
        image = request.files['image'].read()
        input_image = f"data:image/png;base64,{b64encode(image).decode('utf-8')}"
        wavelet_img = wt(image)
        return render_template("wavelet-transform.html", form = form, input_image = input_image, wavelet_img = wavelet_img)
    return render_template("wavelet-transform.html", form = form, input_image = input_image)


@app.route("/harnverhalt", methods=["GET"])
def harnverhalt():
    # Task 5

    return render_template("harnverhalt.html")


@app.route("/cmp", methods=["POST", "GET"])
def cmp():        
    return render_template("cmp.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
