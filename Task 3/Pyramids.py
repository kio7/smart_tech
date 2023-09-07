import cv2 as cv
import matplotlib.pyplot as plt
import os

def Gaussian(filename, num):
    lis = []
    hr = cv.imread(filename)
    lis.append(hr)

    for _ in range(num):
        lr = cv.pyrDown(hr)
        lis.append(lr)
        hr = lr

    return lis


def Laplacian(filename, num):
    lis = []

    hr = cv.imread(filename)
    lis.append(hr)
    src_gray = cv.cvtColor(hr, cv.COLOR_RGB2GRAY)

    for _ in range(num):
        lr = cv.Laplacian(src_gray, 24, ksize=3)
        lis.append(lr)
        src_gray = lr
    
    return lis


def main():
    """
    To use this program, comment out the method and accomadating variables you do not wish to use. 
    Currently the Laplacian method and variables are commented out, so it's set up to use the Guassian pyramid.
    """

    # "cat" can be changed out for "space" or "house", these are other pictures i have included. However, only use Gaussian for "space".
    # The reason why you do not want to use the Laplacian pyramid on the picture "space" is the color simularities are too high. The result doesn't make any sense to use.
    filename = os.path.join(os.path.dirname(__file__), "cat.jpg")

    """ Gaussian """
    amount = 8
    cols = 3
    rows = 3
    lis = Gaussian(filename, amount)


    """ Laplacian """
    # I'm only doing 3 compressions, because after that point Laplacian doesn't make sense. As it all turns into the same color.
    # amount = 3
    # cols = 2
    # rows = 2
    # lis = Laplacian(filename, amount)


    fig = plt.figure(figsize = (16, 9)) # Screen ratio

    for i, img in enumerate(lis): # Plotting the images.
        fig.add_subplot(rows, cols, i+1)
        plt.imshow(img)

    plt.show() # show the plot.


if __name__ == '__main__':
    main()
