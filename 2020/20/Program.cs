using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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
        public List<int[]> Orientations;
        public int[] DistinctValues;

        public int[] Placement { get; private set; } = null;

        public int[] SideValues { get; private set; } = null;
        public Piece[] Adjacent { get; private set; } = null;

        public bool Placed {get ; private set; } = false;

        public bool IsCorner { get {return EdgeCount() == 2; }}
        public bool IsEdge { get {return EdgeCount() == 1; }}

        public Piece(int number, List<string> lines) {
            Number = number;

            SideValues = new int[4];
            Adjacent = new Piece[4];

            Orientations = new List<int[]>();
            var normalOrientation = new int[4];
            var flippedSides = new int[4];

            // Top
            var topString = lines[0].Replace('#', '1').Replace('.','0');
            Console.WriteLine(topString);
            Console.WriteLine(topString.Reverse().ToArray());
            Console.WriteLine("-------");
            normalOrientation[0] = Convert.ToInt32(topString, 2);
            flippedSides[0] = Convert.ToInt32(new string(topString.Reverse().ToArray()), 2);

            // Right
            var rightString = new string(lines.Select(line => line.Last()).ToArray()).Replace('#', '1').Replace('.','0');
            normalOrientation[1] = Convert.ToInt32(rightString, 2);
            flippedSides[1] = Convert.ToInt32(new string(rightString.Reverse().ToArray()), 2);

            // Bottom
            var bottomString = lines.Last().Replace('#', '1').Replace('.','0');
            normalOrientation[2] = Convert.ToInt32(bottomString, 2);
            flippedSides[2] = Convert.ToInt32(new string(bottomString.Reverse().ToArray()), 2);
            // flippedSides[2] = Convert.ToInt32(bottomString, 2);
            // normalOrientation[2] = Convert.ToInt32(new string(bottomString.Reverse().ToArray()), 2);

            // Left
            var leftString = new string(lines.Select(line => line.First()).ToArray()).Replace('#', '1').Replace('.','0');
            normalOrientation[3] = Convert.ToInt32(leftString, 2);
            flippedSides[3] = Convert.ToInt32(new string(leftString.Reverse().ToArray()), 2);
            // flippedSides[3] = Convert.ToInt32(leftString, 2);
            // normalOrientation[3] = Convert.ToInt32(new string(leftString.Reverse().ToArray()), 2);

            Orientations.Add(normalOrientation);
            Orientations.Add(new int[4] { flippedSides[0], flippedSides[3], flippedSides[2], flippedSides[1] });

            // Orientations.Add(normalOrientation);
            // Orientations.Add(new int[4] { normalOrientation[2], flippedSides[1], normalOrientation[0], flippedSides[3] });
            // Orientations.Add(new int[4] { flippedSides[0], normalOrientation[3], flippedSides[2], normalOrientation[1] });
            // Orientations.Add(new int[4] { flippedSides[2], flippedSides[3], flippedSides[0], flippedSides[1] });
            
            DistinctValues = new int[8] {
                normalOrientation[0],
                normalOrientation[1],
                normalOrientation[2],
                normalOrientation[3],
                flippedSides[0],
                flippedSides[1],
                flippedSides[2],
                flippedSides[3]
            };
        }

        public void OrientFirstPiece() {
            for (int i = 0; i < 4; i++) {
                Orient(Orientations[0][i], i);
            }
        }

        // Sets edges to -1
        public void SquashEdges(Dictionary<int, List<Piece>> edgeMapping) {
            foreach (var orientation in Orientations) {
                for (var i = 0; i < 4; i++) {
                    if (edgeMapping[orientation[i]].Count == 1) {
                        orientation[i] = -1;
                    }
                }
            }
        }

        public void Orient(int value, int position) {
            Console.WriteLine($"ORIENT ENTRY : {this} {position} -> {value}");
            // Why we would Orient the same value/position twice, I don't know, but just ignore it.
            if (SideValues[position] == value) {
                return;
            }

            if (SideValues[position] != 0) {
                throw new Exception("Attempting to orient a piece with a value in a position already containing a value");
            }

            // RECORD THE REQUIREMENT
            SideValues[position] = value;
            Console.WriteLine($"ORIENT VALUES: {this} {String.Join(", ",SideValues)}");

            // SHORT CIRCUIT AN ALREADY MATCH
            if (Placement != null && Placement[position] == value) {
                return;
            }

            var matchingOrientations = Orientations
                .Where(orientation => Enumerable.All(Enumerable.Range(0,4), i => SideValues[i] == 0 || orientation.Contains(SideValues[i])));
            if (matchingOrientations.Count() == 0) {
                throw new Exception("Could not find an orientation with all of the required values");
            }

            foreach (var matchingOrientation in matchingOrientations) {
                Console.WriteLine($" -- Trying: {String.Join(", ",matchingOrientation)}");
                // ROTATE THE PIECE INTO Placement
                var valueLocationIndex = 0;
                for (;valueLocationIndex < 4; valueLocationIndex++) {
                    if (matchingOrientation[valueLocationIndex] == value) {
                        var rotation = (valueLocationIndex - position) % 4;
                        rotation = rotation < 0 ? rotation + 4 : rotation;

                        Placement = new int[4];
                        var j = 0;
                        for (var i = rotation; i < 4; i++, j++) {
                            Placement[j] = matchingOrientation[i];
                        }
                        for (var i = 0; i < rotation; i++, j++) {
                            Placement[j] = matchingOrientation[i];
                        }

                        Console.WriteLine($" -- Result: {String.Join(", ",Placement)}");

                        if (Enumerable.All(Enumerable.Range(0,4), i => SideValues[i] == 0 || Placement[i] == SideValues[i])) {
                            // We found the right mix.
                            return;
                        }     
                    }
                }
            }

            throw new Exception("Failed to find a rotation for the piece that works");
        }

        public override string ToString() {
            if (this.Placement == null) {
                var builder = new StringBuilder();
                foreach (var orientation in Orientations) {
                    builder.Append($" [{String.Join(", ", orientation)}]");
                }
                return $"{Number}:{builder.ToString()}";
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

        public int EdgeCount() {
            // if (Placement != null) {
            //     return Placement.Where(i => edgeMapping[i].Count == 1).ToList();    
            // }
            // return Orientations[0].Where(i => edgeMapping[i].Count == 1).ToList();
            return Orientations[0].Count(i => i == -1);
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var mapping = new Dictionary<int, List<Piece>>();
            var pieces = Piece.ParseInput(System.IO.File.ReadAllLines("test.txt"));
            Console.WriteLine($"Total Pieces: {pieces.Count}");
            foreach (var piece in pieces) {
                // piece.Print();
                foreach (var value in piece.DistinctValues) {
                    if (!mapping.ContainsKey(value)) {
                        mapping[value] = new List<Piece>();
                    }
                    mapping[value].Add(piece);
                }
            }

            // // Debug output to show that we have exactly the right number of connections...
            // foreach (var entry in mapping) {
            //     Console.WriteLine($"COUNT {entry.Value.Count}: {entry.Key}");
            // }

            foreach (var piece in pieces) {
                piece.SquashEdges(mapping);
            }

            var cornerPieces = pieces.Where(piece => piece.EdgeCount() == 2);
            var agg = 1L;
            foreach (var piece in cornerPieces) {
                Console.WriteLine(piece);
                // foreach(var i in piece.Orientations[0].Where(i => mapping[i].Count == 1)) {
                //     Console.WriteLine($"   {i}");
                // }
                agg *= piece.Number;
            }
            Console.WriteLine($"Value: {agg}");



            var lastPiece = cornerPieces.First();
            lastPiece.Orient(-1,2);
            lastPiece.Orient(-1,3);

            // // lastPiece.Orient(lastEdgeValues[0], 2);
            // // lastPiece.Orient(lastEdgeValues[1], 3);
            Console.WriteLine($"-----------Placed: {lastPiece}");

            // Build the frame
            for(int walkDir = 0; walkDir < 4; ) {
                var nextPiece = mapping[lastPiece.Placement[walkDir]].Where(item => item != lastPiece && (item.Adjacent == null || item.Adjacent[(walkDir+2)%4] == null)).FirstOrDefault();
                Console.WriteLine($"  Considering: {nextPiece}");

                lastPiece.Adjacent[walkDir] = nextPiece;
                nextPiece.Adjacent[(walkDir + 2)%4] = lastPiece;

                nextPiece.Orient(lastPiece.Placement[walkDir], (walkDir+2)%4);
                nextPiece.Orient(-1, (walkDir+3)%4);
                if (nextPiece.EdgeCount() == 2) {
                    nextPiece.Orient(-1, walkDir);
                    walkDir++;
                    Console.WriteLine($"Found corner, turning to {walkDir}");
                }

                lastPiece = nextPiece;
                Console.WriteLine($"-----------Placed: {lastPiece}");
            }

            Console.WriteLine("FRAME DONE");

            // Fill in the rows
            var lastRowPiece = cornerPieces.First();
            for (var rowHead = lastRowPiece.Adjacent[0]; ! rowHead.IsCorner; lastRowPiece = rowHead, rowHead = rowHead.Adjacent[0]) {
                Console.WriteLine("Starting Row");
                Console.WriteLine(rowHead);
                for (var piece = rowHead; ; piece = piece.Adjacent[1]) {
                    lastRowPiece = lastRowPiece.Adjacent[1];

                    var nextPiece = mapping[piece.Placement[1]].Where(item => item != piece && (item.Adjacent == null || item.Adjacent[3] == null)).FirstOrDefault();
                    Console.WriteLine($"PLACING: {nextPiece}");
                    Console.WriteLine($"LASTROW: {lastRowPiece}");
                    piece.Adjacent[1] = nextPiece;
                    nextPiece.Adjacent[3] = piece;
                    nextPiece.Orient(piece.Placement[1], 3);
                    nextPiece.Orient(lastRowPiece.Placement[0], 2);
                    Console.WriteLine($"-----------Placed: {nextPiece}");
                    Console.WriteLine("");

                    if (nextPiece.IsEdge) {
                        break;
                    }
                }
                Console.WriteLine("");
            }




            // var workQueue = new Queue<Piece>();
            // var seen = new HashSet<Piece>();

            // var firstPiece = pieces.Where(piece => piece.Number == 3083).First();
            // firstPiece.OrientFirstPiece();
            // workQueue.Enqueue(firstPiece);
            // seen.Add(firstPiece);

            // while(workQueue.Count > 0) {
            //     var piece = workQueue.Dequeue();
            //     Console.WriteLine($"Evaluating piece {piece}");
            //     for (var side = 0; side < 4; side++) {
            //         Console.WriteLine($"  side: {side}");
            //         if (piece.Adjacent[side] == null) {
            //             var otherPiece = mapping[piece.Placement[side]].Where(item => item != piece && (item.Adjacent == null || item.Adjacent[(side+2)%4] == null)).FirstOrDefault();
            //             if (otherPiece != null) {
            //                 try {
            //                     otherPiece.Orient(piece.Placement[side], (side + 2) % 4);
            //                 } catch (Exception e) {
            //                     Console.WriteLine($"    {otherPiece}: Orientation failed");
            //                     continue;
            //                 }
            //                 // Should I do placement on the working piece?  That way all pieces are oriented together?

            //                 piece.Adjacent[side] = otherPiece;
            //                 otherPiece.Adjacent[(side+2)%4] = piece;

            //                 if (!seen.Contains(otherPiece)) {
            //                     seen.Add(otherPiece);
            //                     workQueue.Enqueue(otherPiece);
            //                 }
            //                 Console.WriteLine($"    {otherPiece}: Matched for {side}");
            //             }
            //         } else {
            //             Console.WriteLine($"    {piece.Adjacent[side]}: Already attached on {side}");
            //         }
            //     }
            //     Console.WriteLine($"Finished {piece}");
            //     Console.WriteLine("");
            // }
            // Console.WriteLine("---------------");
            // foreach (var piece in pieces) {
            //     piece.Print();
            // }

            // Console.WriteLine("--------------- CORNERS");

            // var corners = pieces.Where(piece => piece.IsCorner);
            // foreach (var piece in corners) {
            //     Console.WriteLine(piece);
            // }
            // Console.WriteLine(corners.Aggregate(1L, (a, piece) => a * (long)piece.Number));

        }
    }
}
