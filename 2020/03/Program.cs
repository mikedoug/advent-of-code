using System;
using System.Collections.Generic;
using System.Linq;

namespace _03
{
    class Program
    {
        static void Main(string[] args)
        {
            String[] puzzle = System.IO.File.ReadLines("input.txt").ToArray();

            Int64 trees = run_slope(puzzle, 3, 1);
            Console.WriteLine(trees);

            List<Int64> values = new List<Int64>{
                run_slope(puzzle, 1, 1),
                run_slope(puzzle, 3, 1),
                run_slope(puzzle, 5, 1),
                run_slope(puzzle, 7, 1),
                run_slope(puzzle, 1, 2)
            };

            Int64 acc = 1;
            foreach (var value in values) {
                acc *= value;
            }
            Console.WriteLine(acc);
        }

        static Int64 run_slope(String[] puzzle, int jstep, int istep) {
            int j = 0;
            int trees = 0;
            for (int i = 0; i < puzzle.Length; i += istep) {
                if (puzzle[i][j] == '#') {
                    trees++;
                }

                j = (j + jstep) % puzzle[0].Length;
            }
            return trees;
        }
    }
}
