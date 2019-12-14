import math
import itertools

class Component(object):
    def __init__(self, text):
        amt, element = text.split(' ')
        self.amt = int(amt)
        self.element = element

    def __str__(self):
        return f'<{self.amt} {self.element}>'

    def __repr__(self):
        return self.__str__()


class Formula(object):
    def __init__(self, formula):
        components, result = line.strip().split(' => ')
        self.components = [Component(x) for x in components.split(', ')]
        self.result = Component(result)

    def __str__(self):
        return f'Add: {self.components} To Get: {self.result}'
    def __repr__(self):
        return self.__str__()


class Universe(object):
    def __init__(self, formulas):
        self.formulas = {}

        for formula in formulas:
            self.formulas[formula.result.element] = formula


    def calculate(self, desired):
        need = {desired.element: desired}
        have = {}
        ore = 0

        while len(need):
            requested = list(need.values())[0]
            del need[requested.element]

            formula = self.formulas[requested.element]
            multiples = math.ceil(requested.amt / formula.result.amt)

            for component in formula.components:
                if component.element == 'ORE':
                    ore += multiples * component.amt
                else:
                    component_amt = multiples * component.amt

                    if component.element in have:
                        existing = min(have[component.element], component_amt)
                        have[component.element] -= existing
                        component_amt -= existing

                    if component_amt > 0:
                        if component.element in need:
                            need[component.element].amt += component_amt
                        else:
                            need[component.element] = Component(f'{component_amt} {component.element}')

            producing = formula.result.amt * multiples
            if producing > requested.amt:
                if requested.element not in have:
                    have[requested.element] = 0
                have[requested.element] += producing - requested.amt

        return ore

with open("input.txt", "r") as f:
    lines = f.readlines()

formulas = []
for line in lines:
    formulas.append(Formula(line.strip()))

universe = Universe(formulas)

# Stage 1
print (f'Stage 1: {universe.calculate(Component("1 FUEL"))} ORE')

# Stage 2 - Very rudimentary search algorithm
def searchit(fn, start, blocksize):
    for i in itertools.count(start, blocksize):
        if fn(i):
            break

    if blocksize == 1:
        return i
    else:
        return searchit(fn, i - blocksize, max(1, blocksize//10))

fuel = searchit(lambda x: universe.calculate(Component(f'{x} FUEL')) > 1_000_000_000_000, 0, 1_000_000 )
print (f'Stage 2: {fuel-1} FUEL')