using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;


namespace _08
{

    public abstract class CommandBase {
        public string Command { get; }
        public int Arg { get; }
        public int I { get; }
        public int Acc { get; set; }

        public CommandBase(string command, int arg, int i) {
            Command = command;
            Arg = arg;
            I = i;
            Acc = 0;
        }

        virtual public int NextI => throw new NotImplementedException();
        virtual public int NextAcc => throw new NotImplementedException();
        virtual public CommandBase Invert => throw new InvalidOperationException();
    }

    public class CommandJmp : CommandBase{
        public CommandJmp(int arg, int i, int acc=0) : base("jmp", arg, i)  {
            Acc = acc;
        }
        override public int NextI => I + Arg;

        override public int NextAcc => Acc;
        
        override public CommandBase Invert => new CommandNop(Arg, I, Acc);

    }

    public class CommandAcc : CommandBase{
        public CommandAcc(int arg, int i) : base("acc", arg, i)  {
        }
        override public int NextI => I + 1;

        override public int NextAcc => Acc + Arg;
    }

    public class CommandNop : CommandBase{
        public CommandNop(int arg, int i, int acc=0) : base("nop", arg, i)  {
            Acc = acc;
        }

        override public int NextI => I + 1;

        override public int NextAcc => Acc;

        override public CommandBase Invert => new CommandJmp(Arg, I, Acc);
    }


    public static class CommandParser {
        static readonly Regex parse = new Regex(@"^(?<cmd>\S+)\s+(?<arg>[-+]\d+)$");

        public static CommandBase Parse(string line, int i) {
            var matches = parse.Match(line);
            int arg = Int32.Parse(matches.Groups["arg"].Value);
            var command = matches.Groups["cmd"].Value;

            switch (command) {
                case "jmp":
                    return new CommandJmp(arg, i);

                case "acc":
                    return new CommandAcc(arg, i);

                case "nop":
                    return new CommandNop(arg, i);

                default:
                    throw new Exception($"Invalid command type {command}");
            }
        }
    }

    public static class EnumerableExtension {

        public static IEnumerable<TResult> SelectWithCounter<TSource, TResult>(this IEnumerable<TSource> source, Func<TSource, int, TResult> selector)
        {
            var i = 0;
            foreach (var item in source) {
                yield return selector(item, i++);
            }
        }
    }


    class Program
    {
        static void Main() {
            Main1();
            Main2();
        }

        static void Main1()
        {
            var lines = System.IO.File.ReadLines("input.txt")
                .SelectWithCounter((x,i) => CommandParser.Parse(x, i))
                .ToArray();

            var SeenIndexes = new HashSet<int>();
            var current = lines[0];

            while(true)
            {
                if (SeenIndexes.Contains(current.I)) {
                    Console.WriteLine($"Repeating index {current.I}, Accumulator {current.Acc}");
                    break;
                }
                SeenIndexes.Add(current.I);

                var i = current.NextI;
                var acc = current.NextAcc;

                if (i >= lines.Length) {
                    Console.WriteLine("Program never looped.");
                    return;
                }

                current = lines[i];
                current.Acc = acc;
            }
        }

        static void Main2()
        {
            var lines = System.IO.File.ReadLines("input.txt")
                .SelectWithCounter((x,i) => CommandParser.Parse(x, i))
                .ToArray();

            var seenIndexes = new HashSet<int>();
            var stack = new List<CommandBase>();
            var lastDepth = -1;
            string lastRemovalInfo = "";

            stack.Add(lines[0]);

            while(true)
            {
                var current = stack.Last();
                int nextI = current.NextI;

                if (nextI == lines.Length) {
                    Console.WriteLine(lastRemovalInfo);
                    Console.WriteLine($"Program worked: ACC={current.Acc}");
                    return;
                }

                CommandBase next = lines[nextI];

                if (seenIndexes.Contains(next.I)) {
                    // If this is our first rewinding, start with the end of the stack
                    if (lastDepth == -1) {
                        lastDepth = stack.Count;
                    }

                    // Rewind the stack 1 step beyond the last attempt
                    lastDepth--;
                    stack.RemoveRange(lastDepth, stack.Count - lastDepth);

                    // Skip any "acc" commands
                    while (stack.Last().Command == "acc") {
                        lastDepth--;
                        stack.RemoveRange(lastDepth, stack.Count - lastDepth);
                    }

                    // Make a new instance with the modified command so our original is untouched.
                    var newLine = stack.Last().Invert;
                    stack.RemoveAt(stack.Count - 1);
                    stack.Add(newLine);

                    lastRemovalInfo = $"{newLine.I} {newLine.Command} {newLine.Arg}";

                    // Reseed our infinite loop detection set
                    seenIndexes = stack.Select(item => item.I).ToHashSet();
                } else {
                    // Add the command to the stack
                    stack.Add(next);
                    // record the ACC for future stack unwinding
                    next.Acc = current.NextAcc;
                    // Flag it as seen
                    seenIndexes.Add(next.I);
                }
            }
        }
    }
}
