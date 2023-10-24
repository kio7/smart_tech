from baseconfig import app

# Imports from our own files
from wavelet import wavelet_transform_mra as wtmra
from wavelet import wavelet_transform as wt
from FFT import fft_quantization_huffman
from our_DCT import dct_quantization
from Task_5 import harnverhalt_roi as hh

from flask import render_template, request
from base64 import b64encode
from forms import waveletImageForm, DCTImageForm, RegionOfInterestForm, FFTImageForm


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/fft", methods=["GET", "POST"])
def fft():
    form = FFTImageForm()
    input_image = None
    output = None

    if form.validate_on_submit():
        image = form.image.data.read()
        output = fft_quantization_huffman(image)
        input_image = f"data:image/png;base64,{b64encode(image).decode('utf-8')}"
        return render_template("fft_and_huffman.html", form=form, output=output, input_image=input_image)
    return render_template("fft_and_huffman.html", form=form, output=output, input_image=input_image)


@app.route("/dct", methods=["GET", "POST"])
def dct():
    form = DCTImageForm()
    input_image = None
    output = None

    if form.validate_on_submit():
        image = form.image.data.read()
        user_input = form.select.data
        output = dct_quantization(image, user_input)
        input_image = f"data:image/png;base64,{b64encode(image).decode('utf-8')}"
        return render_template("dct.html", form=form, output=output, input_image=input_image)
    return render_template("dct.html", form=form, output=output, input_image=input_image)


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


@app.route("/harnverhalt", methods=["POST", "GET"])
def harnverhalt():
    form = RegionOfInterestForm()
    images = None
    if form.validate_on_submit():
        morph = form.morphological.data
        sift = form.sift.data
        imagess = hh.harnverhalt_ROI(morph, sift)
        return render_template("harnverhalt.html", form=form, images=imagess)
    
    return render_template("harnverhalt.html", form=form, images=images)


@app.route("/cmp", methods=["POST", "GET"])
def cmp():        
    return render_template("cmp.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
