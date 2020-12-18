using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace _18
{

    class Token {
        public char Kind {get; init;}
        public long _value;
        public long Value {
            get {
                if (Kind != '#') {
                    throw new Exception("Attempting to get the value of a non numeric Token");
                }

                return _value;
            }
        }

        public Token(string item) {
            long value;
            if (Int64.TryParse(item, out value)) {
                Kind = '#';
                _value = value;
            } else {
                Kind = item[0];
            }
        }

        public static readonly Regex regex = new Regex(@"([)()]|\*|\+|[0-9]+)");
        public static List<Token> ParseLine(string line) {
            return regex.Matches(line).Select(match => new Token(match.Groups[1].Value)).ToList();
        }

        override public string ToString() {
            if (Kind != '#') {
                return $"{Kind}";
            }
            return $"{Value}";
        }

        public Token evaluate(Token operandA, Token operandB) {
            long value;
            switch(Kind) {
                case '+':
                    value = operandA.Value + operandB.Value;
                    break;
                case '*':
                    value = operandA.Value * operandB.Value;
                    break;
                default:
                    throw new Exception($"Invalid operation: {this}");
            }

            return new Token($"{value}");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
             var sum = System.IO.File.ReadLines("input.txt").Select(line => Process2(Token.ParseLine(line))).Sum();
             Console.WriteLine($"Sum: {sum}");

        }

        static long Process1(List<Token> tokens) {
            var stack = new Stack<Token>();
            stack.Push(new Token("1"));
            stack.Push(new Token("*"));

            foreach (var token in tokens) {
                // Console.WriteLine($"Foreach: {token}");
                var evaluate_token = token;

                if (token.Kind == ')') {
                    evaluate_token = stack.Pop();
                    var paren = stack.Pop();
                    if (paren.Kind != '(') {
                        throw new Exception("Close paren without open paren");
                    }
                }
                // Console.WriteLine($"Last: {stack.First()}");
                if (evaluate_token.Kind == '#' && stack.First().Kind != '(') {
                    var op = stack.Pop();
                    var operand = stack.Pop();
                    stack.Push(op.evaluate(operand, evaluate_token));
                } else {
                    stack.Push(evaluate_token);
                }
            }

            if (stack.Count != 1) {
                throw new Exception("Stack has more than one thing left in it, too many open parens?");
            }

            return stack.Pop().Value;
        }

        static long Process2(List<Token> tokens) {
            var stack = new Stack<Token>();
            stack.Push(new Token("1"));
            stack.Push(new Token("*"));

            foreach (var token in tokens) {
                var evaluate_token = token;

                if (token.Kind == ')') {
                    evaluate_token = stack.Pop();
                    while (true) {
                        var op = stack.Pop();
                        if (op.Kind == '(') {
                            break;
                        }
                        var operand = stack.Pop();
                        evaluate_token = op.evaluate(operand, evaluate_token);
                    }
                }
                if (evaluate_token.Kind == '#' && stack.First().Kind != '(' && stack.First().Kind != '*') {
                    var op = stack.Pop();
                    var operand = stack.Pop();
                    stack.Push(op.evaluate(operand, evaluate_token));
                } else {
                    stack.Push(evaluate_token);
                }
            }

            while(stack.Count > 1) {
                var operandB = stack.Pop();
                var op = stack.Pop();
                var operandA = stack.Pop();
                stack.Push(op.evaluate(operandA, operandB));
            }

            return stack.Pop().Value;
        }

    }
}
