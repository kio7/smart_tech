using System;
using System.Collections.Generic;

// Copyright 2017 Valentin Messias https://github.com/messiasv/Huffman/blob/master/LICENSE

namespace E_Helse.Shared.HuffmanCompression
{
    class Code : List<bool>
    {
        public override string ToString()
        {
            string _str = "";
            foreach(bool b in this)
            {
                if (b) _str += "1";
                else _str += "0";
            }
            return _str;
        }
    }
}
