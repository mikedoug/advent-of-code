using System;
using System.Text.RegularExpressions;

namespace _25
{
    class Program
    {
        static void Main(string[] args)
        {
            long key1 = 15733400;
            long key2 = 6408062;

            // long key1 = 5764801;
            // long key2 = 17807724;

            long loopSize1 = 0, loopSize2 = 0;

            long value = 1;
            for (int i = 1; (loopSize1 == 0 || loopSize2 == 0) ; i++) {
                value = (value * 7) % 20201227;

                if (value == key1) {
                    loopSize1 = i;
                }
                if (value == key2) {
                    loopSize2 = i;
                }
            }

            Console.WriteLine($"Loop sizes: {loopSize1} {loopSize2}");

            long key = 1;
            for (int i = 0; i < loopSize1; i++) {
                key = (key * key2) % 20201227;
            }

            Console.WriteLine($"Key: {key}");

        }
    }
}
