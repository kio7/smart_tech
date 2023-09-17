using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

// Copyright 2017 Valentin Messias https://github.com/messiasv/Huffman/blob/master/LICENSE

namespace E_Helse.Shared.HuffmanCompression
{
    public class HuffmanData
    {
        public byte[] compressedData;
        public byte[] uncompressedData;
        public int sizeOfUncompressedData;
        public List<KeyValuePair<byte, int>> frequency;
    }
   
    public class HuffEncoder
    {
        public bool Compress(HuffmanData data)
        {
            FrequencyTable frequencyTable = new FrequencyTable();
            foreach (byte b in data.uncompressedData)
            {
                frequencyTable.Add(b);
            }

            /*
             * Creation of the forest which is represented by a list of binary trees.
             * We add one BinaryTree containing one Node representing a symbol for all the different possible symbols (byte).
             * Each Node will thus have its symbol (byte) and its frequency (int).
             */
            Forest forest = new Forest();
            foreach (byte b in frequencyTable.Keys) forest.Add(new BinaryTree(new Node(b, frequencyTable[b])));

            /*
             * This function is in charge of getting a unique binary tree from all the binary trees contained in the Forest.
             * While the Forest has several trees, we remove the two trees containing the two nodes that have the lowest frequency
             * and assign them to the left and right nodes of the root of a new BinaryTree that we finally had to the forest.
             */
            BinaryTree binaryTree = forest.GetUniqueTree();

            /*
             * This is where the Huffman codes are created.
             * We go all through our BinaryTree thanks to the classic preorder method.
             * When we reach a leaf, we add our code to dictionaries that we'll be using to compress our data.
             * A code is represented by a List of Boolean.
             */
            forest.Preorder(binaryTree.Root, new Code());
            Dictionary<Byte, Code> codeTable = forest.getCodeTable();
            Dictionary<Code, Byte> decodeTable = forest.getDecodeTable();

            /*
             * We get the number of bytes that are required to store our compressed data on a array of bytes.
             * To do it, for each symbol (byte), we multiply its number of occurrences in our uncompressed data by the number of Boolean
             * used to code the symbol. If the result is divisible by eight, we proceed to the division and this is our seeked number. If not,
             * we add one extra byte.
             */
            int GetRequiredBytesNumber()
            {
                int size = 0;
                foreach (Byte b in frequencyTable.Keys) size += frequencyTable[b] * codeTable[b].Count;
                return size % 8 == 0 ? size / 8 : size / 8 + 1;
            }

            int RequiredBytesNumber = GetRequiredBytesNumber();

            /*
             * Here starts the compressing.
             */
            Byte[] compressedData = new Byte[RequiredBytesNumber];

            /*
             * First, for all our symbols in our uncompressed data, let's add their Huffman code to a List of Booleans.
             * This List only contains the bits that are very significant according to our Huffman Code.
             */
            List<bool> compressedDataBoolean = new List<bool>();
            foreach (Byte b in data.uncompressedData)
            {
                compressedDataBoolean.AddRange(codeTable[b]);
            }
            int sizeDataUncompressed = compressedDataBoolean.Count;

            /*
             * This function will put all the booleans contained in our list, in bytes (eight by eight) to store them into
             * an array of bytes.
             */
            Byte[] BooleanListToByteArray(List<bool> boolList)
            {
                Byte[] _compressedData = new Byte[RequiredBytesNumber];
                Byte curr = 0;
                int i = 0, j = 0;
                Boolean b;
                while (boolList.Count > 0)
                {
                    b = boolList.Last();
                    boolList.RemoveAt(boolList.Count - 1);
                    if (i == 0)
                    {
                        // If we iterate over a boolean that must be the first to be put in a byte ...
                        curr = new byte();
                        curr = 0x0;
                    }
                    if (b)
                    {
                        // If our boolean is true, then we need to put a one in our byte at the right position.
                        curr = (Byte)((1 << i) | curr);
                    }
                    else
                    {
                        // Same if it's false.
                        curr = (Byte)((0 << i) | curr);
                    }
                    if (i == 7)
                    {
                        // If we iterate over a boolean that will fill our byte, then we add the byte to our array.
                        _compressedData[j] = curr;
                        j++;
                        i = 0; // We get the 'byte pointer' ready for the next one.
                    }
                    else
                    {
                        i++;
                    }
                }
                // If we didn't get enough booleans to fill the final byte,
                // we had the byte to the array (the other bits of the byte are zero by default).
                if (i != 0) _compressedData[j] = curr;
                return _compressedData;
            }

            compressedData = BooleanListToByteArray(compressedDataBoolean);
            /*
             * We need to pass our frequency table as a List<KeyValuePair<Byte, int>>.
             * It's required by the struct used by the tool.
             */
            List<KeyValuePair<Byte, int>> frequency = frequencyTable.ToList();

            data.compressedData = compressedData;
            data.frequency = frequency;
            data.sizeOfUncompressedData = data.uncompressedData.Length;
            return true;
        }

    }





}
