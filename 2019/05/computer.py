import sys

class Computer(object):
    def __init__(self, memory):
        # We always copy the passed-in memory so that we never harm the caller
        self.memory = list(memory)
        self.i = 0

    def _next_instruction(self):
        instruction = self.memory[self.i]
        opcode = instruction % 100
        modes = list(map(lambda x: int(x), str(instruction)[:-2]))
        # print (f'Modes: {modes}')
        # print (f'Opcode: {opcode}')

        self.current_parameter_position = 0
        self.current_parameter_modes = modes
        self.i += 1

        return opcode

    def _next_mode(self):
        if len(self.current_parameter_modes) > 0:
            return self.current_parameter_modes.pop(-1)

        return 0

    def _get_parameter(self):
        value = self.memory[self.i]
        mode = self._next_mode()

        # Position Mode
        if mode == 0:
            value = self.memory[value]
        # Immediate Mode
        elif mode == 1:
            pass
        else:
            raise Exception(f"Invalid Mode: {mode}")

        self.i += 1
        return value

    def _get_dest_parameter(self):
        value = self.memory[self.i]
        self._next_mode() # Throw away
        self.i += 1

        return value

    def execute(self):
        while self.memory[self.i] != 99:
            # print(f'I: {self.i}')
            # print(self.memory)
            opcode = self._next_instruction()

            # ADD
            if opcode == 1:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = parameter1 + parameter2

            # MULTIPLY
            elif opcode == 2:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = parameter1 * parameter2

            # Opcode 3 takes a single integer as input and saves it to the
            # address given by its only parameter. For example, the
            # instruction 3,50 would take an input value and store it at
            # address 50.
            elif opcode == 3:
                dest = self._get_dest_parameter()
                print("Enter value:")
                self.memory[dest] = int(sys.stdin.readline().rstrip())

            # Opcode 4 outputs the value of its only parameter. For example,
            # the instruction 4,50 would output the value at address 50.
            elif opcode == 4:
                src = self._get_parameter()
                print(f'OUTPUT: {src}')

            # Opcode 5 is jump-if-true: if the first parameter is non-zero,
            # it sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
            elif opcode == 5:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()

                if parameter1 != 0:
                    self.i = parameter2

            # Opcode 6 is jump-if-false: if the first parameter is zero,
            # it sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
            elif opcode == 6:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()

                if parameter1 == 0:
                    self.i = parameter2

            # Opcode 7 is less than: if the first parameter is less than the
            # second parameter, it stores 1 in the position given by the third
            # parameter. Otherwise, it stores 0.
            elif opcode == 7:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = 1 if parameter1 < parameter2 else 0

            # Opcode 8 is equals: if the first parameter is equal to the second
            # parameter, it stores 1 in the position given by the third parameter.
            # Otherwise, it stores 0.
            elif opcode == 8:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = 1 if parameter1 == parameter2 else 0

            else:
                raise Exception(f'Invalid Op: {opcode}')


with open("program.txt", "r") as f:
    memory = list(map(lambda x: int(x), f.readline().rstrip().split(",")))

# print(memory)
# print()

computer = Computer(memory)
computer.execute()
# print(computer.memory)