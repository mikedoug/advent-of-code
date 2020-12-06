using System;
using System.Collections.Generic;

namespace _03
{

    public record House
    {
        public int x { get; init; }
        public int y { get; init; }
    }

    class Program
    {

        static void Main(string[] args)
        {
            var houses = new HashSet<House>();
            
            var input = System.IO.File.ReadAllText("data/input");
            House[] players = new House[2];
            players[0] = players [1] = new House{ x = 0, y = 0};

            houses.Add(players[0]);
            houses.Add(players[1]);

            int current_player = 0;
            foreach (var c in input) {
                switch (c)
                {
                    case '>':
                        players[current_player] = players[current_player] with { y = players[current_player].y + 1 };
                        break;
                    case '<':
                        players[current_player] = players[current_player] with { y = players[current_player].y - 1 };
                        break;
                    case '^':
                        players[current_player] = players[current_player] with { x = players[current_player].x + 1 };
                        break;
                    case 'v':
                        players[current_player] = players[current_player] with { x = players[current_player].x - 1 };
                        break;
                }
                houses.Add(players[current_player]);

                current_player = (current_player + 1) % 2;
            }
            
            Console.WriteLine(houses.Count);
        }

        static void Main1(string[] args)
        {
            var houses = new HashSet<House>();
            
            var input = System.IO.File.ReadAllText("data/input");
            int x = 0, y = 0;
            houses.Add(new House {x = x, y = y});
            foreach (var c in input) {
                switch (c)
                {
                    case '>':
                        y += 1;
                        break;
                    case '<':
                        y -= 1;
                        break;
                    case '^':
                        x += 1;
                        break;
                    case 'v':
                        x -= 1;
                        break;
                }
                houses.Add(new House {x = x, y = y});
            }
            
            Console.WriteLine(houses.Count);
        }
    }
}
