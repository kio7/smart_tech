import os
import cv2 as cv
import numpy as np
from collections import Counter
import os

# Taken from submission 1
# Object with leaf-nodes, left and right
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return self.left, self.right

# Taken from submission 1
def huffman_code_tree(node, binString=''):
    '''
    Function to find Huffman Code
    '''
    # If 'node' has no leaf-nodes, return
    if type(node) is str:
        return {node: binString}
    # Leaf-nodes are assigned to left and right
    (l, r) = node.children()
    # Make an empty dictionary
    d = dict()
    # Update either overwrites or inserts new values into dictionary of nodes
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d

# Taken from submission 1
def make_tree(nodes):
    '''
    Function to make tree
    :param nodes: Nodes
    :return: Root of the tree
    '''
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]


def main():
    # Choose what photo to use:
    path = os.path.join(os.path.dirname(__file__), f"photos/01.jpg")

    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"

    # FFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)


    # Quantization, High pass filter for FFT
    rows, cols = img.shape
    crow, ccol = rows//2 , cols//2
    V1 = 200
    V2 = 201
    # Adjusting the numbers below changes the rate of compression, but large changes are needed to see a difference.
    fshift[crow-V1:crow+V2, ccol-V1:ccol+V2] = 0


    # Huffman code from submission 1 made my Mathias:
    img_string = np.array2string(fshift) # Convert into a hashable/string

    # First makes a table of the symbols with frequency
    freq = dict(Counter(img_string))
    # Sort the dictionary by value frequency, descending order
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    # Create a tree of the frequency table
    node = make_tree(freq)
    encoding = huffman_code_tree(node)
    
    final_result = ""
    for i in img_string:
            final_result = final_result + encoding[i]
    
    #Show original and encoded sizes, and the compression ratio
    input_size_bytes = len(img_string)
    encoded_size_bytes = len(final_result) // 8 
    compression_ratio = input_size_bytes / encoded_size_bytes
    print(f'Size of input string in bytes: {input_size_bytes} \nSize of output string in bytes: {encoded_size_bytes} \nCompression ratio: {compression_ratio}')


if __name__ == '__main__':
    main()
