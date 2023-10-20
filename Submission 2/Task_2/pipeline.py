import os
import cv2
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

# Choose a photo
filename = "01.jpg"
# filename = "02.jpg"
path = os.path.join(os.path.dirname(__file__), f"photos/{filename}")
# Load the original photo
original_image = cv2.imread(path)
gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Apply the DCT to the ROI
dct = cv2.dct(np.float32(gray))

# Perform the inverse DCT on the DCT coefficients
roi_reconstructed = cv2.idct(dct)

# Variables needed for different filters.
rows, cols = gray.shape
crow, ccol = rows//2 , cols//2
V1 = 10
# C2, R2 = 200, 300 # passive
C2, R2 = 310, 600 # Agressive


# High
high = deepcopy(dct)
# Adjusting the numbers below changes the rate of compression, but large changes are needed to see a difference.
high[0:V1, 0:V1] = 0
high_back = cv2.idct(high)
high_img = np.real(high_back)


# Low
low = deepcopy(dct)
# Adjusting the numbers below changes the rate of compression, but large changes are needed to see a difference.
low[len(dct)-C2:, len(dct)-R2:] = 0

low_back = cv2.idct(low)
low_img = np.real(low_back)


# High and low
high_low = deepcopy(dct)
# Adjusting the numbers below changes the rate of compression, but large changes are needed to see a difference.
high_low[0:V1, 0:V1] *= 0.1
high_low[len(dct)-C2:, len(dct)-R2:] = 0

high_low_back = cv2.idct(high_low)
high_low_img = np.real(high_low_back)


# Display the images
plt.figure(figsize=(17, 8))

plt.subplot(231), plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(232), plt.imshow(np.log(np.abs(dct)), cmap='gray')
plt.title('DCT Coefficients')

plt.subplot(233), plt.imshow(roi_reconstructed, cmap='gray')
plt.title('Inverse DCT of gray')

plt.subplot(234), plt.imshow(high_img, cmap='gray')
plt.title('High pass')

plt.subplot(235), plt.imshow(low_img, cmap='gray')
plt.title('Low pass')

plt.subplot(236), plt.imshow(high_low_img, cmap='gray')
plt.title('High and low pass')



plt.tight_layout()
plt.show()
