using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace _02
{
    class Program
    {
        static void Main(string[] args)
        {
            Regex regex = new Regex("^(?<min>[0-9]+)-(?<max>[0-9]+) (?<char>.): (?<str>.*)$");
            // 13-14 m: wfwvfxmchplldvm

            int lineMatches = 0;
            int part2Matches = 0;
            foreach(var line in System.IO.File.ReadLines("input.txt")) {
                var match = regex.Match(line);
                if (!match.Success) {
                    Console.WriteLine($"Failed to match: {line}");
                    return;
                }

                var min = Int32.Parse(match.Groups["min"].Value);
                var max = Int32.Parse(match.Groups["max"].Value);
                var character = match.Groups["char"].Value;
                var s = match.Groups["str"].Value;

                // Part 1
                var count = s.Count(x => x == character[0]);
                if (count >= min && count <= max) {
                    lineMatches++;
                }

                // Part 2
                min--; max--;
                if ((s[min] == character[0] || s[max] == character[0]) && s[min] != s[max]) {
                    part2Matches++;
                }
            }

            Console.WriteLine($"Part 1 Matches: {lineMatches}");
            Console.WriteLine($"Part 2 Matches: {part2Matches}");
        }
    }
}
