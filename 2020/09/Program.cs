using System;
using System.Collections.Generic;
using System.Linq;

namespace _09
{
    class Program
    {

        static void Main() {
            Main1();
            Main2();
        }
        static void Main2()
        {
            var numbers = System.IO.File.ReadLines("input.txt")
                .Select(line => Int64.Parse(line))
                .ToList();

            var workingSet = new List<long>();
            
            int next = 0;
            long value = 0;
            long TARGET = 2089807806L;

            while (value != TARGET) {
                if (value < TARGET) {
                    if (next == numbers.Count){
                        break;
                    }
                    workingSet.Add(numbers[next]);
                    value += numbers[next];
                    next++;
                } else {
                    value -= workingSet[0];
                    workingSet.RemoveAt(0);
                }
            }

            if (value != TARGET) {
                Console.WriteLine("Did not find target");
            } else {
                Console.WriteLine($"{workingSet.Min() + workingSet.Max()}");
            }


        }

        static void Main1()
        {
            var numbers = System.IO.File.ReadLines("input.txt")
                .Select(line => Int64.Parse(line))
                .ToList();

            for (var i = 25; i < numbers.Count; i++) {
                var last25 = numbers.Skip(i-25).Take(25).ToList();
                last25.Sort();

                int a = 0, b = last25.Count - 1;
                while (a != b) {
                    var value = last25[a] + last25[b];
                    if (value == numbers[i]) {
                        break;
                    } else if (value < numbers[i]) {
                        a++;
                    } else {
                        b--;
                    }
                }

                // Solution not found
                if ( a == b ) {
                    Console.WriteLine($"Bad number: {numbers[i]} on line {i+1}");
                    return;
                }

            }
        }
    }
}
