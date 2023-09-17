using System;

// Copyright 2017 Valentin Messias https://github.com/messiasv/Huffman/blob/master/LICENSE

namespace E_Helse.Shared.HuffmanCompression
{
    class BinaryTree : IComparable
    {
        public Node Root { get; set; }

        public BinaryTree(Node root)
        {
            Root = root;
        }

        public int CompareTo(object obj)
        {
            return Root.CompareTo((obj as BinaryTree).Root);
        }

        public override string ToString()
        {
            return Root.ToString();
        }
    }
}
