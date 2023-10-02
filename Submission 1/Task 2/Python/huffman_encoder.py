from collections import Counter
import os, sys

# Object with leaf-nodes, left and right
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return self.left, self.right


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
    # Read input from input.txt
    with open(os.path.join(sys.path[0], "input.txt"), 'r', encoding="utf-8") as f:
        string = f.read()

    # Execute the algorithm
    # First makes a table of the symbols with frequency
    freq = dict(Counter(string))
    # Sort the dictionary by value frequency, descending order
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    # Create a tree of the frequency table
    node = make_tree(freq)
    encoding = huffman_code_tree(node)

    # Write decoding keys, values to codes.txt
    with open(os.path.join(sys.path[0], "codes.txt"), 'w', encoding="utf-8") as f:
        for i in encoding:
            f.write(f'{encoding[i]} : {i}\n')

    # Write the encoded data as binary to output.bin
    with open(os.path.join(sys.path[0], "output.bin"), 'wb') as f:
        output = ""
        for i in string:
            output = output + encoding[i]

        b = bytearray()
        for i in range(0, len(output), 8):
            b.append(int(output[i:i+8], 2))

        f.write(bytes(b))
    
    #Show original and encoded sizes, and the compression ratio
    input_size_bytes = len(string)
    encoded_size_bytes = len(output) // 8 
    compression_ratio = input_size_bytes / encoded_size_bytes
    print(f'Size of input string in bytes: {input_size_bytes}\nSize of output string in bytes: {encoded_size_bytes}\nCompression ratio: {compression_ratio}')


if __name__ == '__main__':
    main()