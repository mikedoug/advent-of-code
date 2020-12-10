using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace _10
{

    class Node
    {
        public int Number {get; private set;}
        private long DynamicSolution = -1;

        List<Node> children;

        // private static readonly Regex r = new Regex("^(?<number>[0-9]*)(?<unit>[a-z]*)$");

        public Node(int number) {
            Number = number;
            children = new List<Node>();
        }

        public void AddChild(Node child) {
            children.Add(child);
        }

        public long CountSolutions(int depth = 0) {

            if (children.Count == 0) {
                return 1;
            }

            if (DynamicSolution == -1) {
                DynamicSolution = children.Sum(c => c.CountSolutions(depth+1));
            }

            return DynamicSolution;
        }
    }

    class Program
    {
        static void Main()
        {
            // Main1();
            Main2();
        }

        static void Main1()
        {
            var numbers = System.IO.File.ReadLines("input.txt")
                .Select(line => Int32.Parse(line))
                .ToList();

            numbers.Sort();

            var differences = new int[4];

            int last = 0;
            foreach(var number in numbers) {
                differences[number-last]++;
                last = number;
            }
            differences[3]++;
            
            Console.WriteLine($"{differences[1] * differences[3]}");
        }

        static void Main2()
        {
            var nodes = System.IO.File.ReadLines("input.txt")
                .Union(new string[]{"0"})
                .Select(line => new Node(Int32.Parse(line)))
                .OrderBy(node => node.Number)
                .ToList();

            var lastThree = new List<Node>();

            // Iterate across the nodes...
            foreach(var node in nodes) {
                // Look at only the last three (because only they can be within the -3 range)
                foreach(var previous in lastThree) {
                    // If it's within range, then add me as a child
                    if (previous.Number >= node.Number - 3) {
                        previous.AddChild(node);
                    }
                }

                // Add myself to the last three list, and remove one if the count goes above 3
                lastThree.Add(node);
                if (lastThree.Count > 3) {
                    lastThree.RemoveAt(0);
                }
            }

            Console.WriteLine(nodes[0].CountSolutions());

        }
    }
}
