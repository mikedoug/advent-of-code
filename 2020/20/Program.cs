using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace _20
{
    public static class RegexExtension {
        public static IEnumerable<Match> MatchOverlap(this Regex regex, string input) {
            Match matchObj = regex.Match(input);
            yield return matchObj;
            while (matchObj.Success) {
                matchObj = regex.Match(input, matchObj.Index + 1); 
                yield return matchObj;
            }
        }

        public static IEnumerable<int> AllIndexes(this String input, char find) {
            int offset = input.IndexOf(find);
            while(offset != -1) {
                yield return offset;
                if (offset + 1 < input.Length) {
                    offset = input.IndexOf(find, offset + 1);
                } else {
                    offset = -1;
                }
            }
        }
    }
    enum SIDES {
        TOP = 0,
        RIGHT,
        BOTTOM,
        LEFT
    }

    class Orientation {
        public int[] Sides;
        public bool Flip;
        public int Rotations;

        public Orientation(int[] sides, bool flip, int rotations) {
            Sides = sides;
            Flip = flip;
            Rotations = rotations;
        }
    }

    class Piece
    {
        public int Number {get; init;}
        public List<Orientation> Orientations;
        public int[] DistinctValues;

        public Orientation Placement { get; set; } = null;

        public int[] SideValues { get; private set; } = null;
        public Piece[] Adjacent { get; private set; } = null;

        public bool Placed {get ; private set; } = false;

        public bool IsCorner { get {return EdgeCount() == 2; }}
        public bool IsEdge { get {return EdgeCount() == 1; }}

        public List<string> Lines;

        public Piece(int number, List<string> lines) {
            Number = number;
            Lines = lines;

            SideValues = new int[4];
            Adjacent = new Piece[4];

            Orientations = new List<Orientation>();
            var normalOrientation = new int[4];
            var flippedSides = new int[4];

            // Top
            var topString = lines[0].Replace('#', '1').Replace('.','0');
            var A = Convert.ToInt32(topString, 2);
            var Ai = Convert.ToInt32(new string(topString.Reverse().ToArray()), 2);

            // Right
            var rightString = new string(lines.Select(line => line.Last()).ToArray()).Replace('#', '1').Replace('.','0');
            var B = Convert.ToInt32(rightString, 2);
            var Bi = Convert.ToInt32(new string(rightString.Reverse().ToArray()), 2);

            // Bottom
            var bottomString = lines.Last().Replace('#', '1').Replace('.','0');
            var C = Convert.ToInt32(bottomString, 2);
            var Ci = Convert.ToInt32(new string(bottomString.Reverse().ToArray()), 2);

            // Left
            var leftString = new string(lines.Select(line => line.First()).ToArray()).Replace('#', '1').Replace('.','0');
            var D = Convert.ToInt32(leftString, 2);
            var Di = Convert.ToInt32(new string(leftString.Reverse().ToArray()), 2);

            Orientations.Add(new Orientation(new int[4] { A,  B,  C,  D  }, false, 0)); // Natural
            Orientations.Add(new Orientation(new int[4] { Di, A,  Bi, C  }, false, 1)); // Natural + Rotate 1
            Orientations.Add(new Orientation(new int[4] { Ci, Di, Ai, Bi }, false, 2)); // Natural + Rotate 2
            Orientations.Add(new Orientation(new int[4] { B,  Ci, D,  Ai }, false, 3)); // Natural + Rotate 3

            Orientations.Add(new Orientation(new int[4] { Ai, D,  Ci, B  }, true, 0)); // Flipped Vertical
            Orientations.Add(new Orientation(new int[4] { Bi, Ai, Di, Ci }, true, 1)); // Flipped Vertical + Rotate 1
            Orientations.Add(new Orientation(new int[4] { C,  Bi, A,  Di }, true, 2)); // Flipped Vertical + Rotate 2
            Orientations.Add(new Orientation(new int[4] { D,  C,  B,  A  }, true, 3)); // Flipped Vertical + Rotate 3

            DistinctValues = new int[8] { A, B, C, D, Ai, Bi, Ci, Di };
        }

        // Sets edges to -1
        public void SquashEdges(Dictionary<int, List<Piece>> edgeMapping) {
            foreach (var orientation in Orientations) {
                for (var i = 0; i < 4; i++) {
                    if (edgeMapping[orientation.Sides[i]].Count == 1) {
                        orientation.Sides[i] = -1;
                    }
                }
            }
        }

        public List<string> getLines() {

            var useLines = Lines.Skip(1).Take(Lines.Count - 2);
            if (Placement.Flip) {
                useLines = useLines.Select(line => new String(line.Reverse().ToArray()));
            }
            useLines = useLines.Select(line => new String(line.Skip(1).Take(line.Length-2).ToArray()));
            var size = useLines.First().Length;

            if (Placement.Rotations == 1) {
                var finalLines = new List<string>();
                for (var i = 0; i < size; i++) {
                    finalLines.Add(useLines.Select(line => line[i]).Aggregate("", (a, p) => p+a));
                }
                return finalLines;
            } else if (Placement.Rotations == 2) {
                var finalLines = new List<string>();
                for (var i = size - 1; i > 0; i--) {
                    finalLines = useLines.Select(line => new String(line.Reverse().ToArray())).Reverse().ToList();
                }
                return finalLines;     
            } else if (Placement.Rotations == 3) {
                var finalLines = new List<string>();
                for (var i = 0; i < size; i++) {
                    finalLines.Add(useLines.Select(line => line[size-1-i]).Aggregate("", (a, p) => a+p));
                }
                return finalLines;
            } else {
                return useLines.ToList();
            }
        }

        public int ImageSize() {
            return Lines.Count - 2;
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
            if (Placement != null && Placement.Sides[position] == value) {
                return;
            }

            var matchingOrientations = Orientations
                .Where(orientation => Enumerable.All(Enumerable.Range(0,4), i => SideValues[i] == 0 || orientation.Sides.Contains(SideValues[i])));
            if (matchingOrientations.Count() == 0) {
                throw new Exception("Could not find an orientation with all of the required values");
            }

            foreach (var matchingOrientation in matchingOrientations.Reverse()) {
            // foreach (var matchingOrientation in matchingOrientations) {
                Console.WriteLine($" -- Trying: {String.Join(", ",matchingOrientation.Sides)}");
                if (Enumerable.All(Enumerable.Range(0,4), i => SideValues[i] == 0 || matchingOrientation.Sides[i] == SideValues[i])) {
                    // We found the right mix.
                    Placement = matchingOrientation;
                    Console.WriteLine($" -- Result: {String.Join(", ",Placement)}");
                    return;
                }
            }

            throw new Exception("Failed to find a rotation for the piece that works");
        }

        public override string ToString() {
            if (this.Placement == null) {
                var builder = new StringBuilder();
                foreach (var orientation in Orientations) {
                    builder.Append($" [{String.Join(", ", orientation.Sides)}]");
                }
                return $"{Number}:{builder.ToString()}";
            } else {
                return $"{Number}: [{String.Join(", ", Placement.Sides)}] [{String.Join(", ", Adjacent.Select(piece => piece == null ? 0 : piece.Number))}] [{Placement.Flip} {Placement.Rotations}]";
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
            return Orientations[0].Sides.Count(i => i == -1);
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var mapping = new Dictionary<int, List<Piece>>();
            var pieces = Piece.ParseInput(System.IO.File.ReadAllLines("input.txt"));
            Console.WriteLine($"Total Pieces: {pieces.Count}");
            foreach (var piece in pieces) {
                foreach (var value in piece.DistinctValues) {
                    if (!mapping.ContainsKey(value)) {
                        mapping[value] = new List<Piece>();
                    }
                    mapping[value].Add(piece);
                }
            }

            foreach (var piece in pieces) {
                piece.SquashEdges(mapping);
            }

            var cornerPieces = pieces.Where(piece => piece.EdgeCount() == 2);
            var agg = 1L;
            foreach (var piece in cornerPieces) {
                Console.WriteLine(piece);
                agg *= piece.Number;
            }
            Console.WriteLine($"Value: {agg}");

            var bottomLeftPiece = cornerPieces.Skip(1).First();
            var lastPiece = bottomLeftPiece;
            lastPiece.Orient(-1,2);
            lastPiece.Orient(-1,3);

            Console.WriteLine($"-----------Placed: {lastPiece}");

            // Build the frame
            for(int walkDir = 0; walkDir < 4; ) {
                var nextPiece = mapping[lastPiece.Placement.Sides[walkDir]].Where(item => item != lastPiece && (item.Adjacent == null || item.Adjacent[(walkDir+2)%4] == null)).FirstOrDefault();
                Console.WriteLine($"  Considering: {nextPiece}");

                lastPiece.Adjacent[walkDir] = nextPiece;
                nextPiece.Adjacent[(walkDir + 2)%4] = lastPiece;

                nextPiece.Orient(lastPiece.Placement.Sides[walkDir], (walkDir+2)%4);
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
            var lastRowPiece = bottomLeftPiece;
            for (var rowHead = lastRowPiece.Adjacent[0]; ! rowHead.IsCorner; lastRowPiece = rowHead, rowHead = rowHead.Adjacent[0]) {
                Console.WriteLine("Starting Row");
                Console.WriteLine(rowHead);
                for (var piece = rowHead; ; piece = piece.Adjacent[1]) {
                    lastRowPiece = lastRowPiece.Adjacent[1];

                    var nextPiece = mapping[piece.Placement.Sides[1]].Where(item => item != piece && (item.Adjacent == null || item.Adjacent[3] == null)).FirstOrDefault();
                    Console.WriteLine($"PLACING: {nextPiece}");
                    Console.WriteLine($"LASTROW: {lastRowPiece}");
                    piece.Adjacent[1] = nextPiece;
                    nextPiece.Adjacent[3] = piece;
                    nextPiece.Orient(piece.Placement.Sides[1], 3);
                    nextPiece.Orient(lastRowPiece.Placement.Sides[0], 2);
                    Console.WriteLine($"-----------Placed: {nextPiece}");
                    Console.WriteLine("");

                    if (nextPiece.IsEdge) {
                        break;
                    }
                }
                Console.WriteLine("");
            }

            // Build our image
            var rowHeads = new List<Piece>();
            for(var piece = bottomLeftPiece; piece != null; piece = piece.Adjacent[0]) {
                rowHeads.Insert(0, piece);
            }

            var builders = new StringBuilder[bottomLeftPiece.ImageSize()];

            var thePuzzle = new List<string>();
            Console.WriteLine("");
            foreach (var rowHead in rowHeads) {
                for(int i = 0; i < bottomLeftPiece.ImageSize(); i++) {
                    builders[i] = new StringBuilder();
                }

                Console.WriteLine("-------");
                for (var piece = rowHead; piece != null; piece = piece.Adjacent[1]) {
                    Console.WriteLine(piece);
                    var pieceLines = piece.getLines();
                    for(int i = 0; i < bottomLeftPiece.ImageSize(); i++) {
                        Console.WriteLine($"   {pieceLines[i]}");
                        builders[i].Append(pieceLines[i]);
                    }
                }

                /// Do something with the builders here -- these rows are done
                foreach (var builder in builders) {
                    thePuzzle.Add(builder.ToString());
                }
            }

            Console.WriteLine("------- the puzzle -------");
            foreach (var line in thePuzzle) {
                Console.WriteLine(line);
            }

            var snake1 = new Regex(@".{18}#.");
            var snake2 = new Regex(@"^#....##....##....###$");
            var snake3 = new Regex(@"^.#..#..#..#..#..#...$");

            bool foundSnake = false;
            for(int i = 0; i < thePuzzle.Count - 2; i++) {
                var matches = snake1.MatchOverlap(thePuzzle[i]);
                foreach (Match match in matches) {
                    // Console.WriteLine($"MATCH START: {i} {match.Index}");

                    if (snake2.IsMatch(thePuzzle[i+1].Substring(match.Index, 20))) {
                        // Console.WriteLine("  -- Line 2 matches");
                        if (snake3.IsMatch(thePuzzle[i+2].Substring(match.Index, 20))) {
                            // Console.WriteLine("  -- Line 3 matches");
                            Console.WriteLine($"MATCH: {i} {match.Index}");
                            Console.WriteLine(thePuzzle[i].Substring(match.Index, 20));
                            Console.WriteLine(thePuzzle[i+1].Substring(match.Index, 20));
                            Console.WriteLine(thePuzzle[i+2].Substring(match.Index, 20));

                            foundSnake = true;

                            var x = match.Index;

                            var lineChars = thePuzzle[i].ToArray();
                            lineChars[x+18] = 'O';
                            thePuzzle[i] = new String(lineChars);

                            lineChars = thePuzzle[i+1].ToArray();
                            foreach( var offset in "#....##....##....###".AllIndexes('#')) {
                                lineChars[x+offset] = 'O';
                            }
                            thePuzzle[i+1] = new String(lineChars);

                            lineChars = thePuzzle[i+2].ToArray();
                            foreach( var offset in ".#..#..#..#..#..#...".AllIndexes('#')) {
                                lineChars[x+offset] = 'O';
                            }
                            thePuzzle[i+2] = new String(lineChars);


                        }
                    }
                }
            }

            if (foundSnake) {
                Console.WriteLine("------- the puzzle -------");
                foreach (var line in thePuzzle) {
                    Console.WriteLine(line);
                }

                var result = thePuzzle.Sum(line => line.Count(c => c == '#'));
                Console.WriteLine($"Result: {result}");
            }
        }
    }
}
