using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace _04
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] codes = { "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid" };
            List<string> ignoreCodes = new List<string>{ "cid" };

            var reader = new RecordReader("input.txt");

            int validCount = 0, invalidCount = 0;
            while (! reader.Finished) {
                var rec = reader.read();
                if (rec.Keys.Count == 0) {
                    break;
                }

                var valid = true;
                foreach (var code in codes) {
                    if (! rec.Keys.Contains(code) && ! ignoreCodes.Contains(code)) {
                        valid = false;
                        break;
                    }
                }

                if (valid && validatePart2(rec)) {
                    validCount++;
                } else {
                    invalidCount++;
                }
            }

            Console.WriteLine($"Valid: {validCount}  Invalid: {invalidCount}");
        }

        private static bool inRange(string value, int min, int max) {
            try {
                var intValue = Int32.Parse(value);
                return intValue >= min && intValue <= max;
            } catch {
                return false;
            }
        }

        private static bool validateHgt(string height) {
            // Console.WriteLine($"Height: {height}");
            Regex r = new Regex("^(?<number>[0-9]*)(?<unit>[a-z]*)$");
            var matches = r.Match(height);
            if (matches is null) {
                return false;
            }
            var unit = matches.Groups["unit"].Value;
            var number = matches.Groups["number"].Value;

            // Console.WriteLine($"Number: '{")

            // If cm, the number must be at least 150 and at most 193.
            if (unit == "cm") {
                return inRange(number, 150, 193);
            }

            // If in, the number must be at least 59 and at most 76.
            else if (unit == "in") {
                return inRange(number, 59, 76);
            }

            // It must be 'in' or 'cm'
            else {
                return false;
            }
        }

        private static Regex rHcl = new Regex("^#[0-9a-f]{6}$");
        private static Regex rEcl = new Regex("^(amb|blu|brn|gry|grn|hzl|oth)$");
        private static Regex rPid = new Regex("^[0-9]{9}$");

        private static bool validatePart2(IDictionary<string, string> rec) {
            
            // byr (Birth Year) - four digits; at least 1920 and at most 2002.
            bool byr = rec["byr"].Length == 4 && inRange(rec["byr"], 1920, 2002);
            // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
            bool iyr = rec["iyr"].Length == 4 && inRange(rec["iyr"], 2010, 2020);
            // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
            bool eyr = rec["eyr"].Length == 4 && inRange(rec["eyr"], 2020, 2030);
            // hgt (Height) - a number followed by either cm or in:
            bool hgt = validateHgt(rec["hgt"]);
            // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            bool hcl = rHcl.IsMatch(rec["hcl"]);
            // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            bool ecl = rEcl.IsMatch(rec["ecl"]);
            // pid (Passport ID) - a nine-digit number, including leading zeroes.
            bool pid = rPid.IsMatch(rec["pid"]);
            // cid (Country ID) - ignored, missing or not.
                // nothing needed here

            // Console.WriteLine($"byr: {byr} iyr: {iyr} eyr: {eyr} hgt: {hgt} hcl: {hcl} ecl: {ecl} pid: {pid}");
            return byr && iyr && eyr && hgt && hcl && ecl && pid;
        }
    }

    public class RecordReader
    {
        private IEnumerator<string> lines;
        public bool Finished { get; private set; }

        public RecordReader(string filename) {
            lines = System.IO.File.ReadLines(filename).GetEnumerator();
            Finished = false;
        }

        public IDictionary<string,string> read() {
            var dictionary = new Dictionary<string,string>();
            while(true) {
                if (! lines.MoveNext()) {
                    Finished = true;
                    break;
                }

                string line;
                try {
                    line = lines.Current;
                } catch {
                    // End of file == End of record
                    Finished = true;
                    break;
                }
                // Console.WriteLine($"Line: {line}");

                // End of record
                if (line == "") {
                    break;
                }

                foreach ( var part in line.Split(' ')) {
                    // Console.WriteLine($"Part: {part}");
                    var kv = part.Split(':', 2);
                    dictionary[kv[0]] = kv[1];
                }
            }

            return dictionary;
        }
    }
}
