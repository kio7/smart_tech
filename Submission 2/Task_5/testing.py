import cv2
import numpy as np

def SIFT_matcher():
    target_image = cv2.imread('Submission 2\static\images\harnverhalt\matTeil.jpg')
    template = cv2.imread('Submission 2\static\images\harnverhalt\harnverhalt5.png')


    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
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

    # Debugging: Check the matches
    return cv2.drawMatches(target_gray, keypoints1, template_gray, keypoints2, good_matches, None)

def main():
    img_matches = SIFT_matcher()
    cv2.imshow('Matches', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()