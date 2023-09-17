using System.Collections.Generic;

// Copyright 2017 Valentin Messias https://github.com/messiasv/Huffman/blob/master/LICENSE

namespace E_Helse.Shared.HuffmanCompression
{
    class FrequencyTable : SortedDictionary<byte,int>
    {
        public void Add(byte b)
        {
            if(ContainsKey(b))
            {
                this[b]++;
            }
            else
            {
                Add(b, 1);
            }
        }

        public override string ToString()
        {
            string _ = "";
            foreach(byte b in Keys)
            {
                _ += b + " :" + this[b] + "\n";
            }
            return _;
        }
    }
}
