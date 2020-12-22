using System;
using System.Collections.Generic;
using System.Linq;

namespace _22
{
    class Game2 {
        static int GameCounter = 1;

        public int GameNumber;
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

        public Game2(List<int> player1, List<int> player2) {
            this.Player1 = player1;
            this.Player2 = player2;
            GameNumber = Game2.GameCounter++;
        }

        private UInt64 CalculateHash(string read)
        {
            UInt64 hashedValue = 3074457345618258791ul;
            for(int i=0; i<read.Length; i++)
            {
                hashedValue += read[i];
                hashedValue *= 3074457345618258799ul;
            }
            return hashedValue;
        }

        // Returns winning player #
        public void Play() {
            Console.WriteLine($" === Game {GameNumber} ===");
            Console.WriteLine("");
            var hashes = new HashSet<UInt64>();

            for (var round = 1; Player1.Count > 0 && Player2.Count > 0 ; round++) {
                var player1DeckString = String.Join(", ", Player1);
                var player2DeckString = String.Join(", ", Player2);

                Console.WriteLine($"-- Round {round} (Game {GameNumber}) --");
                Console.WriteLine($"Player 1's deck: {player1DeckString}");
                Console.WriteLine($"Player 2's deck: {player2DeckString}");

                var hash = CalculateHash($"{player1DeckString}--{player2DeckString}");
                if (hashes.Contains(hash)) {
                    Console.WriteLine($"Previously seen card arrangement");
                    Winner = 1;
                    return;
                }
                hashes.Add(hash);

                var card1 = Player1[0];
                Player1.RemoveAt(0);
                var card2 = Player2[0];
                Player2.RemoveAt(0);

                Console.WriteLine($"Player 1 plays: {card1}");
                Console.WriteLine($"Player 2 plays: {card2}");

                // Determine if we do recursive game
                var roundWinner = 0;
                if (card1 <= Player1.Count && card2 <= Player2.Count) {
                    var subGame = new Game2(
                        Player1.Take(card1).ToList(),
                        Player2.Take(card2).ToList()
                    );
                    subGame.Play();
                    roundWinner = subGame.Winner;
                    Console.WriteLine("");
                    Console.WriteLine($"...anyway, back to game {GameNumber}");
                } else {
                    roundWinner = card1 > card2 ? 1 : 2;
                }

                if (roundWinner == 1) {
                    Console.WriteLine($"Player 1 wins round {round} of game {GameNumber}!");
                    Player1.Add(card1);
                    Player1.Add(card2);
                } else {
                    Console.WriteLine($"Player 2 wins round {round} of game {GameNumber}!");
                    Player2.Add(card2);
                    Player2.Add(card1);
                }
                Console.WriteLine("");
            }

            Winner = Player1.Count > 0 ? 1 : 2;
            Console.WriteLine($"The winner of game {GameNumber} is player {Winner}!");
            Console.WriteLine("");
        }

        public void PostGame() {
            Console.WriteLine("== Post-game results ==");
            Console.WriteLine($"Player {Winner} wins!");
            Console.WriteLine($"Player 1's deck: {String.Join(", ", Player1)}");
            Console.WriteLine($"Player 2's deck: {String.Join(", ", Player2)}");            
        }
    }
}
