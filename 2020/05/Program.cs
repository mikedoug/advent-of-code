using System;
using System.Collections.Generic;
using System.Linq;

namespace _05
{
    public record Line(string LineData) {
        public int GetRow() {
            var binary = new String(this.LineData.Where(x => x == 'F' || x == 'B').Select(x => x == 'F' ? '0' : '1').ToArray());
            var value = Convert.ToInt32(binary, 2);
            return value;
        }

        public int GetColumn() {
            var binary = new String(this.LineData.Where(x => x == 'L' || x == 'R').Select(x => x == 'L' ? '0' : '1').ToArray());
            var value = Convert.ToInt32(binary, 2);
            return value;
        }            

        public int GetSeatId() {
            return GetColumn() + GetRow() * 8;
        }

    }

    class Program
    {
        static void Main(string[] args)
        {
            var lines = System.IO.File.ReadLines("input.txt")
                .Select(x => new Line(x))
                .ToList();

            var seatIds = lines.Select(x => x.GetSeatId()).ToList();
            var max = seatIds.Max();
            Console.WriteLine($"Max: {max}");

            for(var i = 0; i < max; i++) {
                if (seatIds.Contains(i-1) && !seatIds.Contains(i) && seatIds.Contains(i+1)) {
                    Console.WriteLine($"Seat: {i}");
                }
            }
            
        }
    }
}
