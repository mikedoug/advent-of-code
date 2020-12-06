using System;
using System.Collections.Generic;
using System.Linq;

namespace _05
{

    public class Group {
        public List<Line> Lines;
        public int Count => Lines.Count;
        public bool IsEmpty => Lines.Count == 0;

        public Group() {
            Lines = new List<Line>();
        }

        public void Add(Line line) {
            Lines.Add(line);
        }

        public HashSet<Char> GetCharacterSet() {
            return Lines.Aggregate(new HashSet<Char>(), (acc, line) => acc.Union(line.Data).ToHashSet());
        }      

        public HashSet<Char> GetUnanimousCharacterSet() {
            return Lines.Skip(1).Aggregate(
                Lines.First().Data.ToHashSet(),
                (acc, line) => acc.Intersect(line.Data).ToHashSet()
            );
        }     
 
        public static List<Group> BuildGroups(List<Line> lines) {
            var groups = new List<Group>();

            var currentGroup = new Group();
            groups.Add(currentGroup);
            foreach(var line in lines) {
                if (line.IsGroupBreak) {
                    currentGroup = new Group();
                    groups.Add(currentGroup);
                } else {
                    currentGroup.Add(line);
                }
            }
            return groups;
        }
    }

    public record Line(string Data) {
        public bool IsGroupBreak => Data == "";
    }

    class Program
    {
        static void Main(string[] args)
        {
            var lines = System.IO.File.ReadLines("input.txt")
                .Select(x => new Line(x))
                .ToList();

            var groups = Group.BuildGroups(lines);

            int totalUnique = groups.Sum((group) => group.GetCharacterSet().Count);
            int totalUnamimous = groups.Sum((group) => group.GetUnanimousCharacterSet().Count);

            Console.WriteLine($"   Unique Total: {totalUnique}");
            Console.WriteLine($"Unanimous Total: {totalUnamimous}");
        }
    }
}
