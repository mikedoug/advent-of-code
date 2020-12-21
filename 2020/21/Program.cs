using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace _21
{
    class Program
    {
        class Food {
            public HashSet<string> Ingredients { get; private set; }
            public HashSet<string> Allergens { get; private set; }
            
            Regex regex = new Regex(@"^(.*) \(contains (.*)\)$");

            public Food(string line) {
                var match = regex.Match(line);
                if (!match.Success) {
                    throw new Exception($"Failed to parse food: {line}");
                }

                Ingredients = match.Groups[1].Value.Split(" ").ToHashSet();
                Allergens = match.Groups[2].Value.Split(", ").ToHashSet();
            }
        }

        static void Main()
        {
            var foods = System.IO.File.ReadLines("input.txt").Select(line => new Food(line));

            var allAllergens = new HashSet<string>();
            var allIngredients = new HashSet<string>();
            foreach (var food in foods) {
                allAllergens.UnionWith(food.Allergens);
                allIngredients.UnionWith(food.Ingredients);
            }

            Console.WriteLine("----------------");
            // Find the unique ingredients that indicate an allergen.
            var allergenDict = new Dictionary<string, HashSet<string>>();
            foreach (var allergen in allAllergens) {
                Console.WriteLine($"Evaluating: {allergen}");
                var ingredientSets = foods.Where(food => food.Allergens.Contains(allergen)).Select(food => food.Ingredients).ToList();
                var foodWithAllergen = ingredientSets.First();
                foreach (var ingredientSet in ingredientSets) {
                    foodWithAllergen.IntersectWith(ingredientSet);
                }
                allergenDict[allergen] = foodWithAllergen;
                Console.WriteLine($"  Found {foodWithAllergen.Count}");
            }

            // When we know which food is tied to an allergen, remove it from the other allergens we are still narrowing down.
            while(Enumerable.Any(allergenDict.Where(entry => entry.Value.Count > 1))) {
                foreach (var solved in allergenDict.Where(entry => entry.Value.Count == 1)) {
                    foreach (var unsolved in allergenDict.Where(entry => entry.Value.Count > 1)) {
                        Console.WriteLine($"Removing {solved.Value.First()}");
                        unsolved.Value.Remove(solved.Value.First());
                    }
                }
            }

            var ingredientWithAllergens = new HashSet<string>();
            foreach (var allergen in allAllergens) {
                Console.WriteLine($"{allergen} {allergenDict[allergen].Count} {allergenDict[allergen].First()}");
                ingredientWithAllergens.Add(allergenDict[allergen].First());
            }

            // Console.WriteLine("----------------  SAFE");
            // foreach (var ingredient in allIngredients.Where(ingredient => ! ingredientWithAllergens.Contains(ingredient))) {
            //     Console.WriteLine(ingredient);
            // }

            var safeIngredientCount = foods.Sum(food => food.Ingredients.Count(ingredient => ! ingredientWithAllergens.Contains(ingredient)));
            Console.WriteLine($"Safe Ingredient Count: {safeIngredientCount}");

            var canonicalList = allAllergens.OrderBy(allergen => allergen).Select(allergen => allergenDict[allergen].First()).ToList();

            Console.WriteLine($"Canonical: {string.Join(",", canonicalList)}");


        }
    }
}
