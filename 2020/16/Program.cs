using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace _16
{
    public class Field {
        public string Name {get; init;}
        public List<Tuple<long,long>> Ranges = new List<Tuple<long,long>>();
        public List<int> PossiblePositions = new List<int>();

        private static Regex regex = new Regex("^(.*): (\\d+)-(\\d+) or (\\d+)-(\\d+)$");

        public Field(string line) {
            var matches = regex.Match(line);
            Name = matches.Groups[1].Value;
            Ranges.Add(new Tuple<long,long>(Int64.Parse(matches.Groups[2].Value), Int64.Parse(matches.Groups[3].Value)));
            Ranges.Add(new Tuple<long,long>(Int64.Parse(matches.Groups[4].Value), Int64.Parse(matches.Groups[5].Value)));
        }

        public bool InRange(long value) {
            return (value >= Ranges[0].Item1 && value <= Ranges[0].Item2) || (value >= Ranges[1].Item1 && value <= Ranges[1].Item2);
        }

        public void CalculatePossiblePositions(List<Ticket> tickets) {
            for(var i = 0; i < tickets[0].ValueCount; i++) {
                if (tickets.Select(ticket => ticket.GetValueAt(i)).All(value => InRange(value))) {
                    PossiblePositions.Add(i);
                }
            }
        }

        public void RemoveUsed(List<int> usedPositions) {
            PossiblePositions.RemoveAll(value => usedPositions.Contains(value));
        }
    }

    public class Ticket {
        public List<long> Values;

        public Ticket(string line) {
            Values = line.Split(",").Select(item => Int64.Parse(item)).ToList();
        }

        public long SumInvalidValues(List<Field> fields) {
            return Values.Where(value => ! fields.Any(field => field.InRange(value))).Sum();
        }

        public long GetValueAt(int position) {
            return Values[position];
        }

        public int ValueCount => Values.Count;
    }    

    class Program
    {
        static void Main(string[] args)
        {
            var yourTicket = "151,71,67,113,127,163,131,59,137,103,73,139,107,101,97,149,157,53,109,61"
                .Split(',')
                .Select(item => Int64.Parse(item))
                .ToList();

            var fields = System.IO.File.ReadLines("input-fields.txt")
                .Select(line => new Field(line))
                .ToList();

            var inputTickets = System.IO.File.ReadLines("input-tickets.txt")
                .Select(line => new Ticket(line))
                .ToList();

            var errorRate = inputTickets
                .Select(ticket => ticket.SumInvalidValues(fields))
                .Sum();
            Console.WriteLine($"Error Rate: {errorRate}");

            var validTickets = inputTickets
                .Where(ticket => ticket.SumInvalidValues(fields) == 0)
                .ToList();

            foreach (var field in fields) {
                field.CalculatePossiblePositions(validTickets);
            }

            while(fields.Any(field => field.PossiblePositions.Count > 1)) {
                var usedPositions = fields.Where(field => field.PossiblePositions.Count == 1).Select(field => field.PossiblePositions[0]).ToList();

                foreach (var field in fields.Where(field => field.PossiblePositions.Count > 1)) {
                    field.RemoveUsed(usedPositions);
                }
            }

            long product = fields.Where(field => field.Name.StartsWith("departure ")).Select(field => yourTicket[field.PossiblePositions[0]]).Aggregate(1L, (a,item) => a * item);
            Console.WriteLine($"Value: {product}");
        }
    }
}
