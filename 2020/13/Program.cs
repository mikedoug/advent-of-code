using System;
using System.Collections.Generic;
using System.Linq;

namespace _13
{
    class Program
    {
        static void Main1(string[] args)
        {
            List<string> lines = System.IO.File.ReadLines("input.txt").ToList();
            var estimate = Int32.Parse(lines[0]);
            var busses = lines[1].Split(",").Where(part => part != "x").Select(part => Int32.Parse(part)).ToList();
            foreach(var bus in busses) {
                var iterations = (float)estimate / bus;
                var fraction = iterations-(int)iterations;
                var timeUntil = fraction * bus;
                var wait = bus - (estimate % bus);
                Console.WriteLine($"{bus}: {iterations} {fraction} {timeUntil} {wait}");
            }
        }


        static void Main(string[] args)
        {
            var busline = System.IO.File.ReadLines("input.txt").ToList()[1];
            // busline = "7,13,x,x,59,x,31,19";
            var busses = busline.Split(",").Select(part => part == "x" ? "-1" : part).Select(part => Int32.Parse(part)).ToList();
            var busMap = new Dictionary<int, int>();
            for(var i = 0; i < busses.Count; i++) {
                if (busses[i] != -1) {
                    busMap[i] = busses[i];
                }
            }

            foreach(var (position, bus) in busMap) {
                Console.WriteLine($"{position} {bus}");
            }


            int biggest = 68;
            for(long currentTime = 181390 + biggest; ; currentTime += 256769) {
                bool success = true;
                foreach (var (position, bus) in busMap) {
                    if ((currentTime - biggest + position) % bus != 0) {
                        success = false;
                        break;
                    }
                }
                if (success) {
                    Console.WriteLine($"Time: {currentTime - biggest}");
                    break;
                }
            }


        }

        static void MainCalculateFirstAndIntervalOfBiggestTwo(string[] args)
        {
            var busline = System.IO.File.ReadLines("input.txt").ToList()[1];
            // busline = "7,13,x,x,59,x,31,19";
            var busses = busline.Split(",").Select(part => part == "x" ? "-1" : part).Select(part => Int32.Parse(part)).ToList();
            var busMap = new Dictionary<int, int>();
            for(var i = 0; i < busses.Count; i++) {
                if (busses[i] != -1) {
                    busMap[i] = busses[i];
                }
            }

            foreach(var (position, bus) in busMap) {
                Console.WriteLine($"{position} {bus}");
            }

            int biggest = 68;
            int count = 0;
            for(long currentTime = busMap[biggest]; ; currentTime += busMap[biggest]) {
                if ((currentTime - biggest + 37) % 433 != 0) {
                    continue;
                }
                Console.WriteLine($"Time: {currentTime - biggest}");
                if (++count == 2) {
                    break;
                }
            }
        }

    }
}
