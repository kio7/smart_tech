# TODO Write a class that holds methods for the 4 different algorithms.

class Encoder():
    def __init__(self, file, type, data): 
        self.file = file # Pass a file as an argument? Alternatively raw data?
        self.type = type # Filetype?
        self.data = data

    def RLE(self):
        data = self.data
        encoded_string = ""
        i = 0
        while (i <= len(data)-1):
            count = 1
            ch = data[i]
            j = i
            '''if the character at the current index is the same as the character at the next index. If the characters are the same, the count is incremented to 1'''
            while (j < len(data)-1):
                if (data[j] == data[j + 1]): 
                    count = count + 1
                    j = j + 1
                else: 
                    break
            '''the count and the character is concatenated to the encoded string'''
            encoded_string = encoded_string + str(count) + ch
            i = j + 1
        return encoded_string
    

    def Arithmetic(self):
        pass
    

    def Huffman(self):
        pass
    

    def Dictionary(self):
        pass
    