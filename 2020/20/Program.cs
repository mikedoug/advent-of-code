using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace _20
{
    enum SIDES {
        TOP = 0,
        RIGHT,
        BOTTOM,
        LEFT
    }

    class Piece
    {
        public int Number {get; init;}
        public int[] NormalSides {get; init;}
        public int[] FlippedSides {get; init;}

        public int[] Placement { get; private set; } = null;
        public Piece[] Adjacent { get; private set; } = null;

        public bool Placed {get ; private set; } = false;

        public bool IsCorner {
            get {
                return Adjacent != null && Adjacent.Count(piece => piece != null) == 2;
            }
        }

        public Piece(int number, List<string> lines) {
            Number = number;
            NormalSides = new int[4];
            FlippedSides = new int[4];

            // Top
            var topString = lines[0].Replace('#', '1').Replace('.','0');
            NormalSides[0] = Convert.ToInt32(topString, 2);
            FlippedSides[0] = Convert.ToInt32(new string(topString.Reverse().ToArray()), 2);

            // Right
            var rightString = new string(lines.Select(line => line.Last()).ToArray()).Replace('#', '1').Replace('.','0');
            NormalSides[1] = Convert.ToInt32(rightString, 2);
            FlippedSides[1] = Convert.ToInt32(new string(rightString.Reverse().ToArray()), 2);

            // Bottom
            var bottomString = lines.Last().Replace('#', '1').Replace('.','0');
            NormalSides[2] = Convert.ToInt32(bottomString, 2);
            FlippedSides[2] = Convert.ToInt32(new string(bottomString.Reverse().ToArray()), 2);

            // Left
            var leftString = new string(lines.Select(line => line.First()).ToArray()).Replace('#', '1').Replace('.','0');
            NormalSides[3] = Convert.ToInt32(leftString, 2);
            FlippedSides[3] = Convert.ToInt32(new string(leftString.Reverse().ToArray()), 2);
        }

        public void Place(bool flipped, int top_side) {
            var side = flipped ? FlippedSides : NormalSides;
            Placement = new int[4];
            var j = 0;
            for (var i = top_side; i < 4; i++, j++) {
                Placement[j] = side[i];
            }
            for (var i = 0; i < top_side; i++, j++) {
                Placement[j] = side[i];
            }
            Adjacent = new Piece[4] {null, null, null, null};
            Placed = true;
        }

        public void PlaceByValue(int value, int position) {
            if (this.Placed) {
                if (Placement[position] != value) {
                    Console.WriteLine("Invalid placement...");
                    var oppositePosition = (position+2) % 4;
                    if (Placement[oppositePosition] == value) {
                        // Attempt to flip!
                        if (Adjacent[position] == null && Adjacent[oppositePosition] == null) {
                            Console.WriteLine("Flipping!");
                            var temp = Placement[position];
                            Placement[position] = Placement[oppositePosition];
                            Placement[oppositePosition] = temp;
                        } else {
                            Console.WriteLine("... Could not FLIP...");
                        }
                    }
                }
            } else {
                var side = FlippedSides.Contains(value) ? FlippedSides : NormalSides;
                var i = 0;
                for (i = 0; i < 4; i++) {
                    if (side[i] == value) {
                        break;
                    }
                }
                if (i == 4) {
                    throw new Exception("Did not find value...");
                }
                var rotation = (i - position) % 4;
                rotation = rotation < 0 ? rotation + 4 : rotation;
                Console.WriteLine($"Rotation: {rotation} -- {String.Join(", ", side)}");
                this.Place(side == FlippedSides, rotation);
            }
        }

        public override string ToString() {
            if (this.Placement == null) {
                return $"{Number}: [{String.Join(", ", NormalSides)}] [{String.Join(", ", FlippedSides)}]";
            } else {
                return $"{Number}: [{String.Join(", ", Placement)}] [{String.Join(", ", Adjacent.Select(piece => piece == null ? 0 : piece.Number))}]";
            }
        }

        public void Print() {
            Console.WriteLine(this);
        }

        static readonly Regex reNumber = new Regex(@"^Tile (\d+):$");
        public static List<Piece> ParseInput(String[] lines) {
            var tileLines = new Dictionary<int, List<string>>();

            int Number = -1;
            foreach(var line in lines) {
                var match = reNumber.Match(line);
                if (match.Success) {
                    Number = Int32.Parse(match.Groups[1].Value);
                    tileLines[Number] = new List<string>();
                } else if (line != "") {
                    tileLines[Number].Add(line);
                }
            }

            return tileLines.Select(entry => new Piece(entry.Key, entry.Value)).ToList();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var mapping = new Dictionary<int, List<Piece>>();
            var pieces = Piece.ParseInput(System.IO.File.ReadAllLines("test.txt"));
            foreach (var piece in pieces) {
                piece.Print();
                foreach (var value in piece.NormalSides.Union(piece.FlippedSides)) {
                    if (!mapping.ContainsKey(value)) {
                        mapping[value] = new List<Piece>();
                    }
                    mapping[value].Add(piece);
                }
            }

            foreach (var entry in mapping) {
                if (entry.Value.Count > 2) {
                    Console.WriteLine($"{entry.Key} {entry.Value.Count}");
                }
            }

            var workQueue = new Queue<Piece>();

            var firstPiece = pieces.Skip(3).First();
            firstPiece.Place(false, 0);
            workQueue.Enqueue(firstPiece);

            while(workQueue.Count > 0) {
                var piece = workQueue.Dequeue();
                Console.WriteLine($"Evaluating piece {piece}");
                for (var side = 0; side < 4; side++) {
                    Console.WriteLine($"  side: {side}");
                    if (piece.Adjacent[side] == null) {
                        var otherPiece = mapping[piece.Placement[side]].Where(item => item != piece && (item.Adjacent == null || item.Adjacent[(side+2)%4] == null)).FirstOrDefault();
                        if (otherPiece != null) {
                            otherPiece.PlaceByValue(piece.Placement[side], (side + 2) % 4);

                            piece.Adjacent[side] = otherPiece;
                            otherPiece.Adjacent[(side+2)%4] = piece;

                            workQueue.Enqueue(otherPiece);
                            Console.WriteLine($"Matched for {side} {otherPiece}");
                        }
                    }
                }
            }
            Console.WriteLine("---------------");
            foreach (var piece in pieces) {
                piece.Print();
            }

            Console.WriteLine("--------------- CORNERS");

            var corners = pieces.Where(piece => piece.IsCorner);
            foreach (var piece in corners) {
                Console.WriteLine(piece);
            }
            Console.WriteLine(corners.Aggregate(1L, (a, piece) => a * (long)piece.Number));

        }
    }
}
