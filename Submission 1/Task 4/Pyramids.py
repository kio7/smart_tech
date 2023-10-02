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

    """ If we want to maintain the resulution: """
    # lis_2 = []
    # for i, elem in enumerate(lis):
    #     for _ in range(i):
    #         elem = cv.pyrUp(elem)
    #     lis_2.append(elem)
    # return lis_2

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
    """ To use this program, provide the necessary input. """
    
    # "cat" can be changed out for "space" or "house", these are other pictures i have included. However, only use Gaussian for "space".
    # The reason why you do not want to use the Laplacian pyramid on the picture "space" is the color simularities are too high. The result doesn't make any sense to use.
    image_choice = int(input("Which image do you want to see?\n1) 'Cat'\n2) 'Space'\n3) 'House'\n\nEnter 1, 2, or 3: \n"))
    match image_choice:
        case 1:
            filename = os.path.join(os.path.dirname(__file__), "cat.jpg")
        case 2:
            filename = os.path.join(os.path.dirname(__file__), "space.jpg")
        case 3:
            filename = os.path.join(os.path.dirname(__file__), "house.jpg")

    method_choice = int(input("Which method do you wish to use?\n1) Gaussian\n2) Laplacian\n\nEnter 1 or 2: \n"))
    match method_choice:
        case 1:
            """ Gaussian """
            amount = 8
            cols = 3
            rows = 3
            lis = Gaussian(filename, amount)
        case 2:
            """ Laplacian """
            # Doing 3 laplacian transformations, because after that point it all turns into the same color.
            amount = 3
            cols = 2
            rows = 2
            lis = Laplacian(filename, amount)


    fig = plt.figure(figsize = (16, 9)) # Screen ratio

    for i, img in enumerate(lis): # Plotting the images
        fig.add_subplot(rows, cols, i+1)
        plt.imshow(img)

    plt.show() # Show the plot


if __name__ == '__main__':
    main()
