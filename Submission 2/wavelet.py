import os
import numpy as np
import pywt
from PIL import Image
import cv2
import pywt
import pywt.data


def wavelet_transform_mra(path):
    # Load your own image (replace 'your_image_path.png' with your image file path)
    your_image = Image.open(path).convert('L')  # Convert to grayscale

    # Convert the PIL image to a NumPy array
    your_image = np.array(your_image)

    # Wavelet transform of the grayscale image, and plot approximation and details
    titles = ['Approximation', 'Horizontal detail', 'Vertical detail', 'Diagonal detail']
    coeffs2 = pywt.dwt2(your_image, 'bior1.3')
    LL, (LH, HL, HH) = coeffs2

    return [LL, LH, HL, HH]


def wavelet_transform(image_path):
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    path = os.path.dirname(__file__)
    meta_info_image_path = "transform.jpg"
    meta_info_image = cv2.imread(os.path.join(path, meta_info_image_path), cv2.IMREAD_GRAYSCALE)

    # Perform 2D wavelet transform (MRA) on the original image
    coeffs2 = pywt.dwt2(original_image, 'haar')
    LL, (LH, HL, HH) = coeffs2

    # Resize the meta-information image to match the shape of LL
    meta_info_resized = cv2.resize(meta_info_image, (LL.shape[1], LL.shape[0]))

    # Exchange the LL (approximation) coefficients with meta-information
    LL_with_meta_info = LL + meta_info_resized

    modified_image = pywt.idwt2((LL_with_meta_info, (LH, HL, HH)), 'haar')
    return modified_image