using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace _05
{
    public class BagDefinition {
        static readonly Regex primary = new Regex(@"^(?<Outer>.*) bags contain (?<Inner>.*?)\.?$");
        static readonly Regex secondary = new Regex(@"^(?<Count>\d+) (?<Bag>.*) bags?$");
        const string NO_OTHER_BAGS = "no other bags";

        public string Outer { get; private set; }

        public Dictionary<string, int> Inner { get; private set; }

        public BagDefinition(string line) {
            Inner = new Dictionary<string,int>();

            var matches = primary.Match(line);
            Outer = matches.Groups["Outer"].Value;
            if (matches.Groups["Inner"].Value != NO_OTHER_BAGS) {
                matches.Groups["Inner"].Value
                    .Split(", ")
                    .ToList()
                    .ForEach(part => {
                        var innerMatches = secondary.Match(part);
                        Inner[innerMatches.Groups["Bag"].Value] = Int32.Parse(innerMatches.Groups["Count"].Value);
                    }
                );

            }
        }

        public int InnerCount(IDictionary<String,BagDefinition> bagDefinitionMap) {
            return Inner.Aggregate(0, (acc, entry) => acc + entry.Value + entry.Value * bagDefinitionMap[entry.Key].InnerCount(bagDefinitionMap));
        }

    }

    class Program
    {
        static void Main(string[] args) {
            Main1();
            Main2();
        }

        static void Main1()
        {
            string ORIGINAL = "shiny gold";

            var bagDefinitions = System.IO.File.ReadLines("input.txt")
                .Select(x => new BagDefinition(x))
                .ToList();

            var seenBags = new HashSet<string>();
            var queue = new Queue<string>();
            queue.Enqueue(ORIGINAL);

            while(queue.Count > 0) {
                var current = queue.Dequeue();
                seenBags.Add(current);
                bagDefinitions
                    .Where((def) => !seenBags.Contains(def.Outer) && def.Inner.ContainsKey(current))
                    .Select((def) => def.Outer)
                    .ToList()
                    .ForEach(bag => queue.Enqueue(bag));
            }

            Console.WriteLine($"Possible bag count: {seenBags.Where(x => x != ORIGINAL).ToList().Count}");
        }

        static void Main2()
        {
            var bagDefinitionMap = System.IO.File.ReadLines("input.txt")
                .Select(x => new BagDefinition(x))
                .ToDictionary(x => x.Outer);

            var ORIGINAL = "shiny gold";
            var originalCount = bagDefinitionMap[ORIGINAL].InnerCount(bagDefinitionMap);

            Console.WriteLine($"{ORIGINAL} Contains: {originalCount}");
        }
    }
}
