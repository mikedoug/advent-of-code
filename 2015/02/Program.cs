using System;
using System.Linq;

namespace _02
{
    class Program
    {
        static void Main(string[] args)
        {
            Int32 totalPaper = 0;
            Int32 totalRibbon = 0;

            foreach (var line in System.IO.File.ReadLines("data/input.txt")){
                var parts = line.Split("x").Select(x => Int32.Parse(x)).OrderBy(x => x).ToList<Int32>();

                var linePaper = 2 * (parts[0] * parts[1] + parts[1] * parts[2] + parts[2] * parts[0]) + parts[0] * parts[1];
                totalPaper += linePaper;

                var lineRibbon = 2 * (parts[0] + parts[1]) + (parts[0]*parts[1]*parts[2]);
                totalRibbon += lineRibbon;
            }

            Console.WriteLine(totalPaper);
            Console.WriteLine(totalRibbon);
        }
    }
}
