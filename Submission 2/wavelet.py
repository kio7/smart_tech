import os
import numpy as np
import pywt
import cv2
import pywt
import pywt.data
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO
from PIL import Image
from base64 import b64encode

def wavelet_transform_mra(image) -> list:
    # Read the image data from the FileStorage object
    image_data = np.fromstring(image, np.uint8)    
    image_data = cv2.imdecode(image_data, cv2.IMREAD_GRAYSCALE)

    # Wavelet transform of the grayscale image, and plot approximation and details
    coeffs2 = pywt.dwt2(image_data, 'bior1.3')
    LL, (LH, HL, HH) = coeffs2

    # Create plots and return as list of images
    titles = ['Approximation', 'Horizontal detail', 'Vertical detail', 'Diagonal detail']
    plots = []

    for i, image in enumerate([LL, LH, HL, HH]):
        fig = Figure(figsize=(16, 9))
        plot = fig.subplots()

        plot.imshow(image, interpolation="nearest", cmap=plt.cm.gray)
        plot.set_title(titles[i], fontsize=20)
        plot.set_xticks([])
        plot.set_yticks([])

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = b64encode(buf.getvalue()).decode('utf-8')
        plots.append(f"data:image/png;base64,{data}")

    return plots


def wavelet_transform(img: str):

    try: 
        # Load an example image
        image_data = np.fromstring(img, np.uint8) 
        original_image = cv2.imdecode(image_data, cv2.IMREAD_GRAYSCALE)

        # Load the image you want to use as meta-information
        path = os.path.dirname(__file__)
        meta_info_image_path = "static/wavelet_transform.jpg"
        meta_info_image = cv2.imread(os.path.join(path, meta_info_image_path), cv2.IMREAD_GRAYSCALE)

        # Perform 2D wavelet transform (MRA) on the original image
        coeffs2 = pywt.dwt2(original_image, 'haar')
        LL, (LH, HL, HH) = coeffs2

        # Resize the meta-information image to match the shape of LL
        meta_info_resized = cv2.resize(meta_info_image, (LL.shape[1], LL.shape[0]))

        # Exchange the LL (approximation) coefficients with meta-information
        LL_with_meta_info = LL + meta_info_resized

        modified_image = pywt.idwt2((LL_with_meta_info, (LH, HL, HH)), 'haar')
        
        fig = Figure(figsize=(16, 10))
        plot = fig.subplots()

        plot.imshow(modified_image, cmap='gray')
        plot.set_title("Wavelet Transform", fontsize=20)
        
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = b64encode(buf.getvalue()).decode('utf-8')
        image = (f"data:image/png;base64,{data}")


        return image
    
    except Exception as e:
        print(e)
        return None