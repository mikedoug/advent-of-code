using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace _24
{
    public static class Extensions {
        public static void EnqueueRange<T>(this Queue<T> queue, IEnumerable<T> items) {
            foreach(var item in items) {
                queue.Enqueue(item);
            }
        }
    }

    public class Tile {
        public int X {get; private set;}
        public int Y {get; private set;}

        Regex regex = new Regex(@"(se|ne|sw|nw|w|e)");

        public Tile(string line) {
            X = 0;
            Y = 0;
            foreach(Match match in regex.Matches(line)) {
                switch(match.Groups[0].Value) {
                    case "ne":
                        X += 1;
                        break;
                    case "e":
                        Y += 1;
                        break;
                    case "se":
                        X -= 1;
                        Y += 1;
                        break;
                    case "sw":
                        X -= 1;
                        break;
                    case "w":
                        Y -= 1;
                        break;
                    case "nw":
                        X += 1;
                        Y -= 1;
                        break;
                    default:
                        throw new Exception($"invalid match {match.Groups[0].Value}");
                }
            }

        }

    }

    class Program
    {
        static void Main(string[] args)
        {
            var tiles = System.IO.File.ReadLines($"input.txt").Select(line => new Tile(line)).ToList();

            var map = new Dictionary<Tuple<int,int>, int>();
            foreach (var tile in tiles) {
                var key = new Tuple<int,int>(tile.X, tile.Y);
                if (!map.ContainsKey(key)) {
                    map[key] = 1;
                } else {
                    map[key] += 1;
                }
            }

            var black = map.Where(entry => entry.Value % 2 == 1).Select(entry => entry.Key);
            Console.WriteLine($"Black cells: {black.Count()}");

            for( var i = 0; i < 100; i++) {
                var flipList = new HashSet<Tuple<int,int>>();
                var queue = new Queue<Tuple<int,int>>();

                queue.EnqueueRange(black);
                foreach(var tile in black) {
                    queue.EnqueueRange(getAdjacent(tile));
                }

                while(queue.Count > 0) {
                    var tile = queue.Dequeue();
                    var count = getAdjacent(tile).Count(adjacentTile => map.ContainsKey(adjacentTile) && map[adjacentTile] % 2 == 1);
                    var color = map.ContainsKey(tile) && map[tile] % 2 == 1 ? "BLACK" : "WHITE";
                    // Console.WriteLine($"Considering: {tile}; count={count}; color={color}");

                    if ( color == "BLACK" && ( count == 0 || count > 2 ) ) {
                        flipList.Add(tile);
                        // Console.WriteLine(" -- Flip");
                    } else if ( color == "WHITE" && count == 2) {
                        flipList.Add(tile);
                        // Console.WriteLine(" -- Flip");
                    }
                }

                foreach(var tile in flipList) {
                    if (!map.ContainsKey(tile)) {
                        map[tile] = 1;
                    } else {
                        map[tile] += 1;
                    }
                }
                black = map.Where(entry => entry.Value % 2 == 1).Select(entry => entry.Key);
            }

            Console.WriteLine($"Black cells: {black.Count()}");

        }

        private static List<Tuple<int,int>> getAdjacent(Tuple<int, int> cell) {
            return new List<Tuple<int,int>>() {
                new Tuple<int, int>(cell.Item1 + 1, cell.Item2),
                new Tuple<int, int>(cell.Item1,     cell.Item2 + 1),
                new Tuple<int, int>(cell.Item1 - 1, cell.Item2 + 1),
                new Tuple<int, int>(cell.Item1 - 1, cell.Item2),
                new Tuple<int, int>(cell.Item1,     cell.Item2 - 1),
                new Tuple<int, int>(cell.Item1 + 1, cell.Item2 - 1)
            };
        }
    }
}
