using System;
using System.Collections.Generic;
using System.Linq;

namespace _22
{
    class Game {
        public List<int> Player1;
        public List<int> Player2;

        public int Winner {get; private set; }
        public List<int> WinningDeck => Winner == 1 ? Player1 : Player2;

        public int Score {
            get {
                var value = WinningDeck.Count;
                var score = 0;
                for(var i = 0; i < WinningDeck.Count; i++) {
                    score += (value - i) * WinningDeck[i];
                }                    
                return score;
            }
        }

        public Game(List<int> player1, List<int> player2) {
            this.Player1 = player1;
            this.Player2 = player2;
        }

        // Returns winning player #
        public int Play() {
            for (var round = 1; Player1.Count > 0 && Player2.Count > 0 ; round++) {
                Console.WriteLine($"-- Round {round} --");
                Console.WriteLine($"Player 1's deck: {String.Join(", ", Player1)}");
                Console.WriteLine($"Player 2's deck: {String.Join(", ", Player2)}");

                var card1 = Player1[0];
                Player1.RemoveAt(0);
                var card2 = Player2[0];
                Player2.RemoveAt(0);

                Console.WriteLine($"Player 1 plays: {card1}");
                Console.WriteLine($"Player 2 plays: {card2}");

                if (card1 > card2) {
                    Console.WriteLine("Player 1 wins the round!");
                    Player1.Add(card1);
                    Player1.Add(card2);
                } else {
                    Console.WriteLine("Player 2 wins the round!");
                    Player2.Add(card2);
                    Player2.Add(card1);
                }
                Console.WriteLine("");
            }

            Winner = Player1.Count > 0 ? 1 : 2;
            return Winner;
        }

        public void PostGame() {
            Console.WriteLine("== Post-game results ==");
            Console.WriteLine($"Player {Winner} wins!");
            Console.WriteLine($"Player 1's deck: {String.Join(", ", Player1)}");
            Console.WriteLine($"Player 2's deck: {String.Join(", ", Player2)}");            
        }
    }
}
