using System;
using System.Collections.Generic;
using System.Linq;

namespace _22
{

    class Program
    {

        static void Main1()
        {
            string input = "input";

            var game = new Game(
                System.IO.File.ReadLines($"{input}-1.txt").Select(line => Int32.Parse(line)).ToList(),
                System.IO.File.ReadLines($"{input}-2.txt").Select(line => Int32.Parse(line)).ToList()
            );
            var winner = game.Play();
            game.PostGame();
            Console.WriteLine($"Score: {game.Score}");
        }

        static void Main()
        {
            string input = "input";

            var game = new Game2(
                System.IO.File.ReadLines($"{input}-1.txt").Select(line => Int32.Parse(line)).ToList(),
                System.IO.File.ReadLines($"{input}-2.txt").Select(line => Int32.Parse(line)).ToList()
            );
            game.Play();
            game.PostGame();
            Console.WriteLine($"Score: {game.Score}");
        }


    }
}
