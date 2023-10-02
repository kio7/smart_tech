using E_Helse.Shared.HuffmanCompression;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

// Taken from https://www.csharpstar.com/csharp-huffman-coding-using-dictionary/

namespace E_Helse.Shared.HuffmanCompression
{
    public class HuffmanTree
{
    private List<Node2> nodes = new List<Node2>();
    public Node2 Root { get; set; }
    public Dictionary<char, int> Frequencies = new Dictionary<char, int>();

    public void Build(string source)
    {
        for (int i = 0; i < source.Length; i++)
        {
            if (!Frequencies.ContainsKey(source[i]))
            {
                Frequencies.Add(source[i], 0);
            }

            Frequencies[source[i]]++;
        }

        foreach (KeyValuePair<char, int> symbol in Frequencies)
        {
            nodes.Add(new Node2() { Symbol = symbol.Key, Frequency = symbol.Value });
        }

        while (nodes.Count > 1)
        {
            List<Node2> orderedNodes = nodes.OrderBy(node => node.Frequency).ToList<Node2>();

            if (orderedNodes.Count >= 2)
            {
                // Take first two items
                List<Node2> taken = orderedNodes.Take(2).ToList<Node2>();

                // Create a parent node by combining the frequencies
                Node2 parent = new Node2()
                {
                    Symbol = '*',
                    Frequency = taken[0].Frequency + taken[1].Frequency,
                    Left = taken[0],
                    Right = taken[1]
                };

                nodes.Remove(taken[0]);
                nodes.Remove(taken[1]);
                nodes.Add(parent);
            }

            this.Root = nodes.FirstOrDefault();

        }

    }

    public BitArray Encode(string source)
    {
        List<bool> encodedSource = new List<bool>();

        for (int i = 0; i < source.Length; i++)
        {
            List<bool> encodedSymbol = this.Root.Traverse(source[i], new List<bool>());
            encodedSource.AddRange(encodedSymbol);
        }

        BitArray bits = new BitArray(encodedSource.ToArray());

        return bits;
    }

    public string Decode(BitArray bits)
    {
        Node2 current = this.Root;
        string decoded = "";

        foreach (bool bit in bits)
        {
            if (bit)
            {
                if (current.Right != null)
                {
                    current = current.Right;
                }
            }
            else
            {
                if (current.Left != null)
                {
                    current = current.Left;
                }
            }

            if (IsLeaf(current))
            {
                decoded += current.Symbol;
                current = this.Root;
            }
        }

        return decoded;
    }

    public bool IsLeaf(Node2 node)
    {
        return (node.Left == null && node.Right == null);
    }

}
}
