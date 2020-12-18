using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using _14_2;


namespace _14
{

    class Mask
    {
        long and = 0xf_ffff_ffffL;
        long or = 0;

        public Mask(string maskStr) {
            if (maskStr.Length != 36) {
                throw new Exception($"Invalid length mask: {maskStr}");
            }

            for (var i = 0; i < maskStr.Length; i++) {
                if (maskStr[i] == '1') {
                    or |= (1L << (35-i));
                } else if (maskStr[i] == '0') {
                    and ^= (1L << (35-i));
                }
            }
        }

        public long Apply(long value) {
            return value & and | or;
        }
    }

    interface ILine {
    }

    class MaskLine : ILine
    {
        static Regex reMaskLine = new Regex("^mask = (?<bits>[X01]+)$");

        public Mask Mask {get; init;}

        public static ILine ParseLine(String line) {
            var matches = reMaskLine.Match(line);
            
            if (!matches.Success) {
                return null;
            }
            Console.WriteLine($"{matches.Groups["bits"].Value}");

            var value = new MaskLine { Mask = new Mask(matches.Groups["bits"].Value) };
            Console.WriteLine(value.Mask);
            return value;
        }
    }

    class MemLine : ILine
    {
        static Regex reMemLine = new Regex("^mem\\[(?<position>\\d+)\\] = (?<value>\\d+)$");

        public long Position {get; init;}
        public long Value {get; init;}

        public static ILine ParseLine(String line) {
            Console.WriteLine(line);
            var matches = reMemLine.Match(line);
            if (!matches.Success) {
                return null;
            }

            return new MemLine {
                Position = Int64.Parse(matches.Groups["position"].Value),
                Value = Int64.Parse(matches.Groups["value"].Value),
            };
        }
    }
 
    static class LineParser {
        public static ILine Parse(String line) {
            ILine parsed = MaskLine.ParseLine(line) ?? MemLine.ParseLine(line);
            if (parsed == null) {
                throw new Exception($"Line does not parse: {line}");
            }

            return parsed;
        }
    }

    class Program
    {
        static void Main() {
            // Stage1();
            Program2.Stage2();
        }
        
        static void Stage1()
        {
            var lines = System.IO.File.ReadLines("input.txt")
                .Select(line => LineParser.Parse(line))
                .ToList();

            Mask mask = null;
            var memory = new Dictionary<long,long>();
            foreach (var line in lines) {
                var maskLine = line as MaskLine;
                if (maskLine != null) {
                    mask = maskLine.Mask;
                }

                var memLine = line as MemLine;
                if (memLine != null) {
                    memory[memLine.Position] = mask.Apply(memLine.Value);
                }
            }

            var sum = memory.Select(item => item.Value).Sum();
            Console.WriteLine($"Sum: {sum}");
        }
    }
}
