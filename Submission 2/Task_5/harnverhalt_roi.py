import cv2
import numpy as np
from base64 import b64encode

"""
 Use the "harnverhalt" image series to detect the ROI. Implement an 
 application which can choose between using morphological operations, 
 feature vectors with SIFT or a combination of it.
"""

def harnverhalt_ROI(morphological_operation, sift):
    target_image = [cv2.imread('Submission 2\static\images\harnverhalt\matTeil.jpg')]
    templates = [cv2.imread(f'Submission 2\static\images\harnverhalt\harnverhalt{i}.png') for i in range(1, 13)]
    match_images = [cv2_to_base64(image) for image in templates]

    if morphological_operation != 0 and sift != 0:
        morphed_images = {}
        # Apply morphological operations to all images
        if morphological_operation == 1:
            morphed_images["target_image"] = erosion(target_image)
            morphed_images["templates"] = erosion(templates)

        elif morphological_operation == 2:
            morphed_images["target_image"] = dilation(target_image)
            morphed_images["templates"] = dilation(templates)

        elif morphological_operation == 3:
            morphed_images["target_image"] = closing(target_image)
            morphed_images["templates"] = closing(templates)

        elif morphological_operation == 4:
            morphed_images["target_image"] = opening(target_image)
            morphed_images["templates"] = opening(templates)

        # Apply SIFT feature matching to the target images
        match_images = SIFT_matcher(morphed_images["target_image"][0], morphed_images["templates"])

    elif morphological_operation != 0 and sift == 0:
        morphed_images = {}
        # Apply morphological operations to all images
        if morphological_operation == 1:
            morphed_images["target_image"] = erosion(target_image[0])
            morphed_images["templates"] = erosion(templates)

        elif morphological_operation == 2:
            morphed_images["target_image"] = dilation(target_image)
            morphed_images["templates"] = dilation(templates)

        elif morphological_operation == 3:
            morphed_images["target_image"] = closing(target_image)
            morphed_images["templates"] = closing(templates)

        elif morphological_operation == 4:
            morphed_images["target_image"] = opening(target_image)
            morphed_images["templates"] = opening(templates)

        match_images = standard_matcher(morphed_images["target_image"], morphed_images["templates"])
    
    elif sift != 0 and morphological_operation == 0:
        match_images = SIFT_matcher(target_image[0], templates)

    elif sift == 0 and morphological_operation == 0:
        match_images = standard_matcher(target_image[0], templates)
    
    
    return match_images
    


def SIFT_matcher(target_image, templates):
    match_images = []
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    for template in templates:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT_create()

        # Find key points and descriptors in both the target and template images
        keypoints1, descriptors1 = sift.detectAndCompute(target_gray, None)
        keypoints2, descriptors2 = sift.detectAndCompute(template_gray, None)

        # Initialize a Brute-Force Matcher
        bf = cv2.BFMatcher()

        matches = bf.knnMatch(descriptors1, descriptors2, k=2)

        # Apply the ratio test to keep only good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        img = cv2.drawMatches(target_image, keypoints1, template, keypoints2, good_matches, None)
        match_images.append(cv2_to_base64(img))
    
    return match_images


def standard_matcher(target_image, templates):
    match_images = []

    target_image = cv2.imread('Submission 2\static\images\harnverhalt\matTeil.jpg')

    for template in templates:
        result = cv2.matchTemplate(target_image, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.65

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))  # Reverse the coordinates

        h, w = target_image.shape[:-1]

        # Create a copy of the template image to draw rectangles on
        matched_image = template.copy()

        # Mark the found locations on the matched image with green rectangles
        for loc in locations:
            top_left = loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(matched_image, top_left, bottom_right, (0, 255, 0), 1)

        match_images.append(cv2_to_base64(matched_image))

    return match_images

# Morphological opertations functions
def erosion(images, kernel_size=5):
    imgs = []
    for image in images:
        if image is not None:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            imgs.append(cv2.erode(image, kernel, iterations=1))
    return imgs

def dilation(images, kernel_size=5):
    imgs = []
    for image in images:
        if image is not None:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            # fix
            imgs.append(cv2.dilate(image, kernel, iterations=1))
    return imgs

def closing(images, kernel_size=5):
    imgs = []
    for image in images:
        if image is not None:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            imgs.append(closed_image)
    return imgs

def opening(images, kernel_size=5):
    imgs = []
    for image in images:
        if image is not None:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
            imgs.append(opened_image)
    return imgs

def cv2_to_base64(image):
    # Convert the OpenCV image to a NumPy array
    image_np = np.asarray(image)
    
    # Encode the NumPy array as a Base64 string
    _, buffer = cv2.imencode('.png', image_np)
    base64_image = b64encode(buffer).decode('utf-8')

    return f'data:image/png;base64,{base64_image}'