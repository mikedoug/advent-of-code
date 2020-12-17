using System;
using System.Linq;

namespace _15
{
    class Program
    {
        static void Main1(string[] args)
        {
            var numbers = "6,19,0,5,7,13,1"
                .Split(',')
                .Select(item => Int64.Parse(item))
                .ToList();

            int target = 2020;

            while(numbers.Count < target) {
                var consider = numbers.Last();

                long age = -1;
                foreach (var pair in numbers.Reverse<long>().Skip(1).Select((number, i) => (number, i))) {
                    if (pair.number == consider) {
                        age = pair.i + 1;
                        break;
                    }
                }

                numbers.Add(age == -1 ? 0 : age);
            }

            Console.WriteLine($"{target}th: {numbers[target-1]}");
        }

        static void Main(string[] args)
        {
            var numbers = "6,19,0,5,7,13,1"
            // var numbers = "0,3,6"
                .Split(',')
                .Select(item => Int32.Parse(item))
                .ToList();

            int target = 30_000_000;
            // target = 2020;
            int firstValue = numbers.First();

            int[] lastSeen = new int[target];

            for(var i = 0; i < numbers.Count - 1; i++) {
                // Console.WriteLine($"{i+1}: {numbers[i]}");
                lastSeen[numbers[i]] = i;
            }

            int currentValue = numbers.Last();
            for(var i = numbers.Count - 1; i < target -1; i++) {
                // Console.WriteLine($"currentValue: {currentValue}");
                // Console.WriteLine($"lastSeen[currentValue]: {lastSeen[currentValue]}");

                int nextValue;
                if (lastSeen[currentValue] == 0 && currentValue != firstValue) {
                    nextValue = 0;
                } else {
                    nextValue = i - lastSeen[currentValue];
                }
                lastSeen[currentValue] = i;
                // Console.WriteLine($"{i+1}: {currentValue}");

                currentValue = nextValue;
            }
            Console.WriteLine($"Final value: {currentValue}");

            // while(numbers.Count < target) {
            //     var consider = numbers.Last();

            //     int age = -1;
            //     foreach (var pair in numbers.Reverse<int>().Skip(1).Select((number, i) => (number, i))) {
            //         if (pair.number == consider) {
            //             age = pair.i + 1;
            //             break;
            //         }
            //     }

            //     numbers.Add(age == -1 ? 0 : age);
            // }

            // Console.WriteLine($"{target}th: {numbers[target-1]}");
        }
    }
}
