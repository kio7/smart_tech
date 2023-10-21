import cv2

"""
 Use the "harnverhalt" image series to detect the ROI. Implement an 
 application which can choose between using morphological operations, 
 feature vectors with SIFT or a combination of it.
"""

class ROIDetector:
    def __init__(self, image, threshold=0.5):
        self.image = image
        self.threshold = threshold
        self.roi = None

    def set_sift_roi(self):
        roi_image = cv2.imread('../static/images/harnverhalt/matTeil.jpg', cv2.IMREAD_GRAYSCALE)
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(roi_image, None)
        self.roi = (kp1, des1)

    def match_SIFT(self):
        self.set_sift_roi()
        sift = cv2.SIFT_create()
        kp2, des2 = sift.detectAndCompute(self.image, None)

        index_params = dict(algorithm=0, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(self.roi[1], des2, k=2)

        good_points = []
        for m, n in matches:
            if m.distance < self.threshold * n.distance:
                good_points.append(m)
                
        return good_points


