using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;

namespace _11
{
    class Program
    {
        const char OUT_OF_BOUNDS = 'X';
        static char GetCell(List<string> lines, int lineNumber, int seat) {
            if (lineNumber < 0 || lineNumber >= lines.Count || seat < 0 || seat >= lines[lineNumber].Length) {
                return OUT_OF_BOUNDS;
            }

            return lines[lineNumber][seat];
        }

        static string processLine1(List<string> lines, int lineNumber) {
            var builder = new StringBuilder();
            for (int c = 0; c < lines[lineNumber].Length; c++) {
                if (lines[lineNumber][c] == '.') {
                    builder.Append('.');
                    continue;
                }

                int count =
                    (GetCell(lines, lineNumber - 1, c - 1) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber - 1, c    ) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber - 1, c + 1) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber + 1, c - 1) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber + 1, c    ) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber + 1, c + 1) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber    , c - 1) =='#' ? 1 : 0) +
                    (GetCell(lines, lineNumber    , c + 1) =='#' ? 1 : 0);

                switch (lines[lineNumber][c]) {
                    case '#':
                        builder.Append(count >= 4 ? 'L' : '#');
                        break;

                    case 'L':
                        builder.Append(count == 0 ? '#' : 'L');
                        break;
                }
            }
            return builder.ToString();
        }


        static bool OccupiedPath(List<string> lines, int lineNumber, int seat, int lineDir, int seatDir) {
            while (true) {
                lineNumber += lineDir;
                seat += seatDir;
                switch (GetCell(lines, lineNumber, seat)) {
                    case '#':
                        return true;

                    case 'L':
                    case OUT_OF_BOUNDS:
                        return false;
                }
            }
        }

        static string processLine2(List<string> lines, int lineNumber) {
            var builder = new StringBuilder();
            for (int seat = 0; seat < lines[lineNumber].Length; seat++) {
                if (lines[lineNumber][seat] == '.') {
                    builder.Append('.');
                    continue;
                }

                int count =
                    (OccupiedPath(lines, lineNumber, seat, 1, 0) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, 1, -1) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, 1, 1) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, -1, 0) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, -1, -1) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, -1, 1) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, 0, -1) ? 1 : 0) +
                    (OccupiedPath(lines, lineNumber, seat, 0, 1) ? 1 : 0);

                switch (lines[lineNumber][seat]) {
                    case '#':
                        builder.Append(count >= 5 ? 'L' : '#');
                        break;

                    case 'L':
                        builder.Append(count == 0 ? '#' : 'L');
                        break;
                }
            }
            return builder.ToString();
        }

        static void Main() {
            Main1();
            Main2();
        }

        static void Main1()
        {
            List<string> lines = System.IO.File.ReadLines("input.txt").ToList();

            List<string> newLines;
            while(true) {
                newLines = Enumerable.Range(0, lines.Count).Select(lineNumber => processLine1(lines, lineNumber)).ToList();

                if (Enumerable.SequenceEqual(lines, newLines)) {
                    break;
                }

                lines = newLines;
            }

            var seats = newLines.Select(line => line.Count(c => c == '#')).Sum();
            Console.WriteLine($"Seats: {seats}");
        }

        static void Main2()
        {
            List<string> lines = System.IO.File.ReadLines("input.txt").ToList();

            List<string> newLines;
            while(true) {
                newLines = Enumerable.Range(0, lines.Count).Select(lineNumber => processLine2(lines, lineNumber)).ToList();

                if (Enumerable.SequenceEqual(lines, newLines)) {
                    break;
                }

                lines = newLines;
            }

            var seats = newLines.Select(line => line.Count(c => c == '#')).Sum();
            Console.WriteLine($"Seats: {seats}");
        }

    }
}
