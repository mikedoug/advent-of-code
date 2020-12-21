using System;
using System.Collections.Generic;
using System.Linq;

namespace _17a
{
    public class Xyz {
        public int X {get; init;}
        public int Y {get; init;}
        public int Z {get; init;}

        public static IEnumerable<Xyz> GetAdjacent(){
            foreach (var x in Enumerable.Range(-1,3)) {
                foreach (var y in Enumerable.Range(-1,3)) {
                    foreach (var z in Enumerable.Range(-1,3)) {
                        if (x != 0 || y != 0 || z != 0) {
                            yield return new Xyz() { X = x, Y = y, Z = z };
                        }
                    }
                }
            }
        }
    }

    class Cube {
        //         Z, X, Y
        private Dictionary<int,bool[][]> Layers;
        public int Offset {get; init;}
        public int Size {get; init;}

        public Cube(int size) {
            Layers = new Dictionary<int,bool[][]>();
            Offset = size / 2;
            Size = size;
        }

        public bool[][] NewLayer(int layerNumber) {
            bool[][] layer = new bool[Size][];
            foreach(var i in Enumerable.Range(0, Size)) {
                layer[i] = new bool[Size];
            }
            Layers[layerNumber] = layer;
            return layer;
        }

        public static Cube FromLines(List<String> lines) {
            var cube = new Cube(lines.Count);
            var layer = cube.NewLayer(0);
            foreach(var x in Enumerable.Range(0, cube.Size)) {
                foreach(var y in Enumerable.Range(0, cube.Size)) {
                    layer[x][y] = lines[x][y] == '#';
                }
            }
            return cube;
        }

        public static Cube FromCube(Cube old) {
            var cube = new Cube(old.Size + 2);
            Enumerable.Range(old.Layers.Keys.Min() - 1, old.Layers.Keys.Count+2).ToList().ForEach(layer => {
                cube.NewLayer(layer);
                cube.CalculateLayer(layer, old);
            });

            return cube;
        }



        public void CalculateLayer(int layer, Cube old) {
            foreach(var x in Enumerable.Range(0, Size)) {
                foreach(var y in Enumerable.Range(0, Size)) {
                    var count = Xyz.GetAdjacent().Select(adj => old.GetActive(x - Offset + adj.X, y - Offset + adj.Y, layer + adj.Z)).Count(active => active == true);
                    var oldValue = old.GetActive(x - Offset, y - Offset, layer);
                    
                    if (oldValue) {
                        Layers[layer][x][y] = count == 2 || count == 3;
                    } else {
                        Layers[layer][x][y] = count == 3;
                    }
                }
            }
        }

        // This is bounds safe
        public bool GetActive(int x, int y, int z) {
            try {
                return Layers[z][x+Offset][y+Offset];
            } catch {
                return false;
            }
        }

        public void Print() {
            foreach(var entry in Layers) {
                Console.WriteLine($"z={entry.Key}");
                foreach(var x in Enumerable.Range(0, Size)) {
                    foreach(var y in Enumerable.Range(0, Size)) {
                        Console.Write(entry.Value[x][y] ? "#" : ".");
                        // Console.Write(GetActive(x-Offset,y-Offset,entry.Key) ? "#" : ".");
                    }
                    Console.WriteLine("");
                }
            }
        }

        public int ActiveCount() {
            return Layers.Sum(entry => entry.Value.Sum(row => row.Sum(value => value ? 1 : 0)));
        }

    }
    class Program
    {

        static void Main(string[] args) {
            using(new TimeIt.TimeIt("Part 1")) {
                Main1(args);
            }
            using(new TimeIt.TimeIt("Part 2")) {
                _17b.Program.Main2(args);
            }
        }

        static void Main1(string[] args)
        {
            var lines = System.IO.File.ReadLines("input.txt")
                .ToList();

            var cube = Cube.FromLines(lines);
            cube.Print();

            foreach( var i in Enumerable.Range(1,6)) {
                cube = Cube.FromCube(cube);
                Console.WriteLine("");
                Console.WriteLine($"Iteration: {i}");
            }

            Console.WriteLine($"Active Count: {cube.ActiveCount()}");

        }
    }
}
