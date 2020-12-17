using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace _12
{
    class Instruction {
        public char Direction {get; init;}
        public int Length {get; init;}

        private static readonly Regex regex = new Regex(@"^([NSEWLRF])(\d+)$");

        public Instruction(string line) {
            var matches = regex.Match(line);
            Direction = matches.Groups[1].Value[0];
            Length = Int32.Parse(matches.Groups[2].Value);
        }

        public override string ToString()
        {
            return $"{Direction}{Length}";
        }
    }

    class Ship {
        public int Facing {get; private set;}
        public int X {get; set;}
        public int Y {get; set;}

        public Ship() {
            Facing = 90;
            X = 0;
            Y = 0;
        }

        public void ProcessInstruction(Instruction instruction) {
            if (instruction.Direction == 'N' || (instruction.Direction == 'F' && Facing == 0)) {
                Y += instruction.Length;
            } else if (instruction.Direction == 'S' || (instruction.Direction == 'F' && Facing == 180)) {
                Y -= instruction.Length;
            } else if (instruction.Direction == 'E' || (instruction.Direction == 'F' && Facing == 90)) {
                X += instruction.Length;
            } else if (instruction.Direction == 'W' || (instruction.Direction == 'F' && Facing == 270)) {
                X -= instruction.Length;
            } else if (instruction.Direction == 'L') {
                Facing -= instruction.Length;
                if (Facing < 0) {
                    Facing += 360;
                }
            } else if (instruction.Direction == 'R') {
                Facing += instruction.Length;
                if (Facing >= 360) {
                    Facing -= 360;
                }
            } else if (instruction.Direction == 'F') {
                throw new Exception($"Invalid facing on F command: {Facing}");
            } else {
                throw new Exception($"Invalid instruction: {instruction.Direction}{instruction.Length}");
            }
        }
    }

    class Waypoint {
        public int X {get; private set;}
        public int Y {get; private set;}
        public Ship Ship { get; private set;}

        public Waypoint() {
            Ship = new Ship();
            X = 10;
            Y = 1;
        }

        public void ProcessInstruction(Instruction instruction) {
            if (instruction.Direction == 'N') {
                Y += instruction.Length;
            } else if (instruction.Direction == 'S') {
                Y -= instruction.Length;
            } else if (instruction.Direction == 'E') {
                X += instruction.Length;
            } else if (instruction.Direction == 'W') {
                X -= instruction.Length;
            } else if ((instruction.Direction == 'L' && instruction.Length == 90) || (instruction.Direction == 'R' && instruction.Length == 270)) {
                (X, Y) = (-Y, X);
            } else if ((instruction.Direction == 'L' || instruction.Direction == 'R') && instruction.Length == 180) {
                (X, Y) = (-X, -Y);
            } else if ((instruction.Direction == 'R' && instruction.Length == 90) || instruction.Direction == 'L' && instruction.Length == 270) {
                (X, Y) = (Y, -X);
            } else if (instruction.Direction == 'F') {
                Ship.X += instruction.Length * X;
                Ship.Y += instruction.Length * Y;
            } else {
                throw new Exception($"Invalid instruction: {instruction.Direction}{instruction.Length}");
            }
        }
    }    

    class Program
    {
        static void Main(string[] args)
        {
            var instructions = System.IO.File.ReadLines("input.txt")
                .Select(line => new Instruction(line))
                .ToList();

            var ship = new Ship();
            foreach (var instruction in instructions) {
                ship.ProcessInstruction(instruction);
            }
            Console.WriteLine($"Part 1: {Math.Abs(ship.X) + Math.Abs(ship.Y)}");
            

            var waypoint = new Waypoint();
            foreach (var instruction in instructions) {
                waypoint.ProcessInstruction(instruction);
            }

            Console.WriteLine($"Part 2: {Math.Abs(waypoint.Ship.X) + Math.Abs(waypoint.Ship.Y)}");

        }
    }
}
