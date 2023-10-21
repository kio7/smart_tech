import os
import numpy as np
import matplotlib.pyplot as plt
import pywt
import cv2


# Load your own image (replace 'your_image_path.png' with your image file path)
path = os.path.dirname(__file__)
image_path = os.path.join(path, 'photos/02.jpg')
# your_image = Image.open(image_path).convert('L')  # Convert to grayscale
your_image = np.array(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))

# Convert the PIL image to a NumPy array
# your_image = np.array(your_image)

# Wavelet transform of the grayscale image, and plot approximation and details
titles = ['Approximation', 'Horizontal detail', 'Vertical detail', 'Diagonal detail']
coeffs2 = pywt.dwt2(your_image, 'bior1.3')
LL, (LH, HL, HH) = coeffs2

fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()


# def wavelet_transform_mra(path):
#     # Load your own image (replace 'your_image_path.png' with your image file path)
#     your_image = Image.open(path).convert('L')  # Convert to grayscale

#     # Convert the PIL image to a NumPy array
#     your_image = np.array(your_image)

#     # Wavelet transform of the grayscale image, and plot approximation and details
#     titles = ['Approximation', 'Horizontal detail', 'Vertical detail', 'Diagonal detail']
#     coeffs2 = pywt.dwt2(your_image, 'bior1.3')
#     LL, (LH, HL, HH) = coeffs2

#     return [LL, LH, HL, HH]
