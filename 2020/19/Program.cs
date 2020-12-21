using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace _19
{
    class RuleEntry
    {
        public int Number {get; init;}
        public string Rule {get; init;}

        public bool IsTerminal => Rule == "\"a\"" || Rule == "\"b\"";
        public char TerminalValue => Rule[1];

        static readonly Regex regex = new Regex("^(\\d+): (.*)$");

        public RuleEntry(string line) {
            var match = regex.Match(line);
            Number = Int32.Parse(match.Groups[1].Value);
            Rule = match.Groups[2].Value;
        }

        public string RegexString(Dictionary<int,RuleEntry> rules, int depth=0) {
            if (IsTerminal) {
                return TerminalValue.ToString();
            }

            var builder = new StringBuilder();
            var hasOr = false;
            foreach (var part in Rule.Split(" ")) {
                if (part == "|") {
                    hasOr = true;
                    builder.Append("|");
                } else {
                    var nextPart = Int32.Parse(part);
                    if(nextPart == Number) {
                        // This is only here to limit the recursion -- I expected to have to
                        // increase this value until I hit a right answer, but 5 was plenty.
                        if (depth == 5) {
                            continue;
                        }
                        builder.Append(rules[nextPart].RegexString(rules, depth + 1));
                    } else {
                        builder.Append(rules[nextPart].RegexString(rules));
                    }
                }
            }
            if (hasOr) {
                return $"(?:{builder.ToString()})";
            }
            return builder.ToString();
        }
    }

    class Program
    {
        static void Main1(string[] args)
        {
            var rules = System.IO.File.ReadLines("testB-1.txt").Select(line => new RuleEntry(line)).ToDictionary(entry => entry.Number);

            var regexString = "^" + rules[0].RegexString(rules) + "$";
            Console.WriteLine(regexString);
            var regex = new Regex(regexString);

            var lines = System.IO.File.ReadLines("testB-2.txt");
            // foreach (var line in lines) {
            //     Console.Write($"{line} -- ");
            //     if (regex.IsMatch(line)) {
            //         Console.WriteLine("Matches");
            //     } else {
            //         Console.WriteLine("Fails");
            //     }
            // }

            var count = lines.Count(line => regex.IsMatch(line));
            Console.WriteLine($"Matches: {count}");
        }

        static void Main(string[] args)
        {
            var rules = System.IO.File.ReadLines("input-1.txt").Select(line => new RuleEntry(line)).ToDictionary(entry => entry.Number);
            rules[8] = new RuleEntry("8: 42 | 42 8");
            rules[11] = new RuleEntry("11: 42 31 | 42 11 31");

            var regexString = "^" + rules[0].RegexString(rules) + "$";
            Console.WriteLine(regexString.Length);
            var regex = new Regex(regexString);

            var count = System.IO.File.ReadLines("input-2.txt").Count(line => regex.IsMatch(line));
            Console.WriteLine($"Matches: {count}");
        }
    }
}
