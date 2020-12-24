using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace _23
{
    static class Extensions {
        public static IEnumerable<long> LongRange(long start, long count)
        {
            var limit = start + count;

            while (start < limit)
            {
                yield return start;
                start++;
            }
        }
    }

    class Node {
        public int Value {get; init;}
        public Node Next;

        public Node(int value) {
            Value = value;
        }

        public override string ToString() {
            return $"{Value}";
        }

        public IEnumerable<Node> Walk() {
            yield return this;
            for (Node ptr = Next; ptr != this; ptr = ptr.Next) {
                yield return ptr;
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var cupsList = "167248359".Select(c => Int32.Parse($"{c}")).Union(Enumerable.Range(10, 1_000_000-9));
            var cups = cupsList.Select(value => new Node(value)).ToList();
            var map = cups.ToDictionary(item => item.Value);

            for (var i = 0; i < cups.Count; i++) {
                cups[i].Next = cups[(i+1) % cups.Count];
            }

            var current = cups[0];
            var largest = cups.Max(item => item.Value);
            
            Console.WriteLine($"{cups.Count}");

            Stopwatch timer = new Stopwatch();
            timer.Start();
            for(long move = 1L; move <= 10_000_000L; move++) {
                // Console.WriteLine($"-- move {move}");

                // Console.WriteLine($"cups: ({current}) {String.Join("  ", map[1].Walk())}");

                var removed1 = current.Next;
                var removed3 = removed1.Next.Next;
                // Console.WriteLine($"pick up: {removed1}, {removed1.Next}, {removed3}");

                // Rewire the head of our cut
                current.Next = removed3.Next;

                // Rewire the tail of our cut
                removed3.Next = null;
                
                var value = (current.Value == 1) ? largest : current.Value - 1;

                Node choosen = null;
                while(choosen == null) {
                    if (value != removed1.Value && value != removed1.Next.Value && value != removed3.Value) {
                        choosen = map[value];
                    } else {
                        value = (value == 1) ? largest : value - 1;
                    }
                }

                // Console.WriteLine($"destination: {value}");
                // Console.WriteLine("");
                
                // rewire it back in
                removed3.Next = choosen.Next;
                choosen.Next = removed1;

                // Move to next cup
                current = current.Next;
            }
            timer.Stop();
            Console.WriteLine($"-- Elapsed: {timer.Elapsed}");

            Console.WriteLine($"cups: {String.Join("  ", map[1].Walk().Take(20))}");
            var one = map[1];
            Console.WriteLine($"Cups-to-right: {one.Next} {one.Next.Next}");
            Console.WriteLine($"Product: {(long)one.Next.Value * (long)one.Next.Next.Value}");
        }
    }
}
