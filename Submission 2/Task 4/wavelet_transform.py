import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Import PyWavelets library
import pywt
import pywt.data

# Load an example image
path = os.path.dirname(__file__)
image_path = "image.jpg"
original_image = cv2.imread(os.path.join(path, image_path), cv2.IMREAD_GRAYSCALE)

# Perform 2D wavelet transform (MRA) on the original image
''' The output is a tuple with 4 elements: LL, (LH, HL, HH)
LL = Approximation, LH = Horizontal detail, HL = Vertical detail, HH = Diagonal detail
"haar" is the name of the wavelet used '''
coeffs2 = pywt.dwt2(original_image, 'haar')
LL, (LH, HL, HH) = coeffs2

# Define meta information (for example, a watermark)
'''Random meta-information is generated using NumPy's 
np.random.randint function. The meta_info variable 
contains random integer values between 0 and 127. 
The goal is to embed this meta-information into the 
approximation component (LL) of the wavelet-transformed image.'''
meta_info = np.random.randint(0, 128, size=LL.shape)  # Ensure meta_info has the same dimensions as LL

# Resize meta_info to match the shape of LL
meta_info_resized = cv2.resize(meta_info, (LL.shape[1], LL.shape[0]))

# Exchange the LL (approximation) coefficients with meta information
LL_with_meta_info = LL + meta_info_resized

# Reconstruct the image using the modified coefficients
'''The modified coefficients, including LL_with_meta_info, 
LH, HL, and HH, are used to reconstruct the modified image 
using the inverse wavelet transform with the 'haar' wavelet. 
The reconstructed image is stored in the modified_image variable.'''
modified_image = pywt.idwt2((LL_with_meta_info, (LH, HL, HH)), 'haar')

# Plot the original and modified images
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(original_image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(modified_image, cmap='gray')
plt.title('Modified Image with Meta Information')
plt.axis('off')

plt.tight_layout()
plt.show()