import cv2
from copy import deepcopy
import numpy as np
from matplotlib.figure import Figure
from io import BytesIO
from base64 import b64encode


def dct_quantization(image, user_input):   
    img = np.fromstring(image, np.uint8)
    gray = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)

    # Apply DCT
    dct = cv2.dct(np.float32(gray))

    # Variables for how aggressive the filters are.
    # Adjusting the numbers below changes the rate of compression, but large changes are needed to see a difference.
    match user_input:
        case 0: C2, R2, V1 = int(gray.shape[0]//5), int(gray.shape[1]//5), 10 # Passive
        case 1: C2, R2, V1 = int(gray.shape[0]/10), int(gray.shape[1]/10), 15 # Agressive
        case 2: C2, R2, V1 = int(gray.shape[0]/20), int(gray.shape[1]/20), 20 # Very agressive

    # High
    high = deepcopy(dct)
    high[0:V1, 0:V1] = 0
    high_back = cv2.idct(high)
    high_img = np.real(high_back)


    # Low
    low = deepcopy(dct)
    low[C2:len(dct), R2:len(dct[0])] = 0
    low_back = cv2.idct(low)
    low_img = np.real(low_back)


    # High and low
    high_low = deepcopy(dct)
    high_low[0:V1, 0:V1] *= 0.1
    high_low[C2:len(dct), R2:len(dct[0])] = 0
    high_low_back = cv2.idct(high_low)
    high_low_img = np.real(high_low_back)


    # Display the images
    titles = ['DCT Coefficients', 'High pass', 'Low pass', 'High and low pass']
    fig = Figure(figsize=(16, 9))

    # DCT Coeff
    plot = fig.add_subplot(221)
    plot.imshow(np.log(np.abs(dct)), cmap='gray')
    plot.set_title(titles[0], fontsize=20)
    
    # High pass
    plot = fig.add_subplot(222)
    plot.imshow(high_img, cmap='gray')
    plot.set_title(titles[1], fontsize=20)

    # Low pass
    plot = fig.add_subplot(223)
    plot.imshow(low_img, cmap='gray')
    plot.set_title(titles[2], fontsize=20)

    # High and low pass
    plot = fig.add_subplot(224)
    plot.imshow(high_low_img, cmap='gray')
    plot.set_title(titles[3], fontsize=20)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = b64encode(buf.getvalue()).decode('utf-8')
    image = (f"data:image/png;base64,{data}")

    return image