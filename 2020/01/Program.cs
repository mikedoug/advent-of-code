using System;
using System.Collections.Generic;
using System.Linq;

namespace _01
{
    class Program
    {
        static void Main1(string[] args)
        {
            var numbers = new List<int>(
                from line in System.IO.File.ReadLines("input.txt")
                select Int32.Parse(line)
            );
            numbers.Sort();

            const int target = 2020;

            int i = 0, j = numbers.Count - 1;
            while(true) {
                if (i == j) {
                    break;
                }

                int total = numbers[i] + numbers[j];

                if (total == target) {
                    Console.WriteLine($"Match found {numbers[i]} * {numbers[j]} = {numbers[i] * numbers[j]}");
                    break;
                }

                if (total > target) {
                    j--;
                } else if (total < target) {
                    i++;
                } else {
                    var idelta = numbers[i+1] - numbers[i];
                    var jdelta = numbers[j] - numbers[j-1];
                    if (idelta < jdelta) {
                        i++;
                    } else {
                        j--;
                    }
                }
            }
        }

        static void Main(string[] args)
        {
            var numbers = new List<int>(
                from line in System.IO.File.ReadLines("input.txt")
                select Int32.Parse(line)
            );
            numbers.Sort();

            const int target = 2020;

            for(var a = 0; a < numbers.Count; a++) {
                int i = 0, j = numbers.Count - 1;
                while(true) {
                    if (i == j) {
                        break;
                    }

                    int total = numbers[i] + numbers[j] + numbers[a];

                    if (total == target) {
                        Console.WriteLine($"Match found {numbers[i]} * {numbers[j]} * {numbers[a]}= {numbers[i] * numbers[j] * numbers[a]}");
                        break;
                    }

                    if (total > target) {
                        j--;
                    } else if (total < target) {
                        i++;
                    } else {
                        var idelta = numbers[i+1] - numbers[i];
                        var jdelta = numbers[j] - numbers[j-1];
                        if (idelta < jdelta) {
                            i++;
                        } else {
                            j--;
                        }
                    }
                }
            }
        }
    }
}
