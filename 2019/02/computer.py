import sys

def run(memory):
    memory = list(memory)

    i = 0
    while memory[i] != 99:
        instruction = memory[i]

        if instruction == 1:
            parameter1 = memory[i+1]
            parameter2 = memory[i+2]
            dest = memory[i+3]

            memory[dest] = memory[parameter1] + memory[parameter2]
            i += 4
        elif instruction == 2:
            parameter1 = memory[i+1]
            parameter2 = memory[i+2]
            dest = memory[i+3]

            memory[dest] = memory[parameter1] * memory[parameter2]
            i += 4
        else:
            raise Exception(f'Invalid Op: {instruction}')

    return memory


memory = list(map(lambda x: int(x), sys.stdin.readline().rstrip().split(",")))
print(memory)
print()

# Step 1
if 0:
    memory[1] = 12
    memory[2] = 2
    print(run(memory))


for a in range(0,100):
    for b in range(0,100):
        testmem = list(memory)
        testmem[1] = a
        testmem[2] = b

        testmem = run(testmem)
        if testmem[0] == 19690720:
            print(f'{a} {b}')
            print(a * 100 + b)
            print(testmem)
            sys.exit(0)
