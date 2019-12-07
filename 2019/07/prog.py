import computer
import itertools

with open("input.txt", "r") as f:
    software = list(map(lambda x: int(x),f.readline().rstrip().split(",")))

outputs = []
for a in range(5):
    program = computer.Computer(software)
    results = program.execute([a, 0])
    outputA = results[0]

    for b in range(5):
        if a == b:
            continue
        program = computer.Computer(software)
        results = program.execute([b, outputA])
        outputB = results[0]

        for c in range(5):
            if c in [a,b]:
                continue
            program = computer.Computer(software)
            results = program.execute([c, outputB])
            outputC = results[0]

            for d in range(5):
                if d in [a, b, c]:
                    continue
                program = computer.Computer(software)
                results = program.execute([d, outputC])
                outputD = results[0]

                for e in range(5):
                    if e in [a, b, c, d]:
                        continue
                    program = computer.Computer(software)
                    results = program.execute([e, outputD])
                    # print(f"{a} {b} {c} {d} {e} -- {outputA} {outputB} {outputC} {outputD} {results[0]}")
                    outputs.append(results[0])

print (f"Maximum output part one: {max(outputs)}")
if max(outputs) != 929800:
    print("^^^^^^ FAIL ^^^^^^")


def feedback_loop(phases):
    programs = []
    for phase in phases:
        program = computer.Computer(software)
        program.safe_execute([phase])

        programs.append(program)

    input = 0
    while True:
        for program in programs:
            program.safe_execute([input])
            input = program.outputs[-1]

        if programs[-1].state == computer.State.HALT:
            return input

outputs = []
for permutation in itertools.permutations([5,6,7,8,9]):
    outputs.append(feedback_loop(permutation))

print (f"Maximum output part two: {max(outputs)}")
if max(outputs) != 15432220:
    print("^^^^^^ FAIL ^^^^^^")



