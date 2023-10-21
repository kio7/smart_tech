from baseconfig import app
from flask import render_template, request
import numpy as np
import cv2
from base64 import b64encode
from io import BytesIO
from forms import waveletImageForm
from wavelet import wavelet_transform_mra




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
        mra = wavelet_transform_mra(image)        
 
        return render_template("wavelet-mra.html", form=form, input_image=input_image, mra = mra)
    return render_template("wavelet-mra.html", form=form, input_image = input_image)

@app.route("/wavelet_transform", methods=["GET"])
def wavelet_transform():
    # Task 4
    
    return render_template("wavelet-transform.html")

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
