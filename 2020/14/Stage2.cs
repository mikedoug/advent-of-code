using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace _14_2
{

    class Mask2
    {
        public string MaskString {get; private set;}

        public Mask2(string maskStr) {
            if (maskStr.Length != 36) {
                throw new Exception($"Invalid length mask: {maskStr}");
            }

            MaskString = maskStr;
        }

        public Mask2 Apply(long value) {
            var builder = new StringBuilder();
            for (var i = 35; i >= 0; i--) {
                builder.Append((value & (1L<<i)) != 0 ? '1' : '0');
            }
            return new Mask2(builder.ToString());
        }

        public List<Mask2> Minus(Mask2 Other) {
            var builders = new List<StringBuilder>();
            builders.Add(new StringBuilder());

            for (var i = 0; i < MaskString.Length; i++) {
                if (MaskString[i] != 'X') {
                    if (MaskString[i] != Other.MaskString[i]) {
                        // If there is ever a bit tye differ on, then the subtraction removes nothing
                        return new List<Mask2>() {this};
                    }
                    foreach (var builder in builders) {
                        builder.Append(MaskString[i]);
                    }
                } else {
                    if (Other.MaskString[i] == 'X') {
                        foreach (var builder in builders) {
                            builder.Append('X');
                        }
                    } else {
                        for(var j = 0; j < builders.Count - 1; j++) {
                            builders[j].Append('X');
                        }
                        builders.Append(new StringBuilder(builders[builders.Count -1].ToString()));
                        builders[builders.Count-2].Append(Other.MaskString[i] == '0' ? '1' : '0');
                        builders[builders.Count-1].Append(Other.MaskString[i]);
                    }
                }
            }
            return builders.Select(builder => new Mask2(builder.ToString())).ToList();
        }

        public long CountOfAddresses() {
            return (long)Math.Pow(2.0, (double)MaskString.Count(c => c == 'X'));
        }

        override public String ToString() {
            return MaskString;
        }

        static Regex reMaskLine = new Regex("^mask = (?<bits>[X01]+)$");

    }

    class MaskLine2 : ILine
    {
        static Regex reMaskLine = new Regex("^mask = (?<bits>[X01]+)$");

        public Mask2 Mask {get; init;}

        public static ILine ParseLine(String line) {
            var matches = reMaskLine.Match(line);
            
            if (!matches.Success) {
                return null;
            }
            Console.WriteLine($"{matches.Groups["bits"].Value}");

            var value = new MaskLine2 { Mask = new Mask2(matches.Groups["bits"].Value) };
            Console.WriteLine(value.Mask);
            return value;
        }
    }    

    interface ILine {
    }    

    class MemLine2 : ILine
    {
        static Regex reMemLine = new Regex("^mem\\[(?<position>\\d+)\\] = (?<value>\\d+)$");

        public Mask2 Mask {get; init;}
        public long Value {get; init;}

        public static ILine ParseLine(Mask2 currentMask, String line) {
            Console.WriteLine(line);
            var matches = reMemLine.Match(line);
            if (!matches.Success) {
                return null;
            }

            return new MemLine2 {
                Mask = currentMask.Apply(Int64.Parse(matches.Groups["position"].Value)),
                Value = Int64.Parse(matches.Groups["value"].Value),
            };
        }
    }

    static class LineParser2 {
        public static Mask2 CurrentMask = null;

        public static ILine Parse(String line) {
            ILine parsed = MaskLine2.ParseLine(line) ?? MemLine2.ParseLine(CurrentMask, line);
            if (parsed == null) {
                throw new Exception($"Line does not parse: {line}");
            }
            if (parsed is MaskLine2) {
                CurrentMask = (parsed as MaskLine2).Mask;
            }

            return parsed;
        }
    }

    public class Program2
    {
        public static void Stage2()
        {
            var masks = System.IO.File.ReadLines("input.txt")
                .Select(line => LineParser2.Parse(line))
                .Where(entry => entry is MemLine2)
                .Select(entry => entry as MemLine2)
                .Select(entry => entry.Mask)
                .ToList();

            var newMasks = new List<Mask2>();
            for (var i = 1; i < masks.Count; i++) {
                for (var j = 0; j < i; j++) {
                    newMasks.AddRange(masks[j].Minus(masks[i]));
                }
            }

            var sum = newMasks.Select(item => item.CountOfAddresses * item.).Sum();
            Console.WriteLine($"Sum: {sum}");
        }
    }
}
