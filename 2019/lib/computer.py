import sys
from collections.abc import MutableMapping
from enum import Enum

class State(Enum):
    INIT = 1  # The computer has been initialized, but not yet executed
    LIVE = 2  # The computer program is actively running
    WAIT = 3  # The computer is waiting for more inputs
    HALT = 99 # The computer program has halted

class Memory(MutableMapping):
    def __init__(self, memory):
        self._PAGE_SIZE = 16
        pages = [list(memory[i:i+self._PAGE_SIZE]) for i in range(0, len(memory), self._PAGE_SIZE)]

        self.memory = dict(zip(range(0, len(pages)), pages))

    def __getitem__(self, position):
        page, offset = divmod(position, self._PAGE_SIZE)
        try:
            return self.memory[page][offset]
        except:
            return 0

    def __setitem__(self, position, value):
        page, offset = divmod(position, self._PAGE_SIZE)
        try:
            self.memory[page][offset] = value
        except:
            self._validate_page_offset(page, offset)
            self.memory[page][offset] = value


    def __delitem__(self, i):
        raise Exception("Not Implemented")

    def __iter__(self):
        raise Exception("Not Implemented")

    def __len__(self):
        raise Exception("Not Implemented -- difficult concept")

    def print(self):
        for index, page in sorted(self.memory.items(), key=lambda x: x[0]):
            print(f'{index * self._PAGE_SIZE:10}: {page}')

    # Grows the memory as needed when references are made outside of the existing memory space
    def _validate_page_offset(self, page, offset):
        if page not in self.memory:
            self.memory[page] = [int(x) for x in '0' * self._PAGE_SIZE]

        # If the page does not include the specific byte, expand the page fully
        elif offset >= len(self.memory[page]):
            self.memory[page] = list(self.memory[page]) + [int(x) for x in '0' * (self._PAGE_SIZE - len(self.memory[page]))]


class Computer(object):

    def __init__(self, memory):
        # We always copy the passed-in memory so that we never harm the caller
        self.memory = Memory(memory)
        self.outputs = []
        self.i = 0
        self.state = State.INIT
        self.trace = False
        self._relative_base = 0

    def _next_instruction(self):
        instruction = self.memory[self.i]
        modes, opcode = divmod(instruction, 100)
        modes = [int(x) for x in reversed(str(modes))]

        self._parameter_modes = modes
        self.i += 1

        return opcode

    def _next_mode(self):
        if len(self._parameter_modes) > 0:
            return self._parameter_modes.pop(0)
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
        elif mode == 2:
            value = self.memory[self._relative_base + value]
        else:
            raise Exception(f"Invalid Mode: {mode}")

        self.i += 1
        return value

    def _get_dest_parameter(self):
        value = self.memory[self.i]
        mode = self._next_mode() # Throw away
        if mode == 1:
            raise Exception(f"Mode for get dest parameter {mode}")
        self.i += 1

        value += (self._relative_base if mode == 2 else 0)
        
        return value

    def execute(self, inputs=None):
        if self.state in [State.INIT, State.WAIT]:
            self.state = State.LIVE
        else:
            raise Exception(f"Attempting to execute program in invalid state: {self.state}")

        while self.state == State.LIVE:
            trace_i = self.i
            opcode = self._next_instruction()

            # ADD
            if opcode == 1:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = parameter1 + parameter2
                if self.trace:
                    print(f"[{trace_i}] ADD {parameter1} + {parameter2} = {self.memory[dest]} --> {dest}")

            # MULTIPLY
            elif opcode == 2:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = parameter1 * parameter2
                if self.trace:
                    print(f"[{trace_i}] MUL {parameter1} * {parameter2} = {self.memory[dest]} --> {dest}")

            # Opcode 3 takes a single integer as input and saves it to the
            # address given by its only parameter. For example, the
            # instruction 3,50 would take an input value and store it at
            # address 50.
            elif opcode == 3:
                dest = self._get_dest_parameter()
                if inputs is None:
                    print("Enter value:")
                    self.memory[dest] = int(sys.stdin.readline().rstrip())
                else:
                    if len(inputs) == 0:
                        self.i -= 2
                        self.state = State.WAIT
                        # raise NeedInput("Out of input!")
                    else:
                        self.memory[dest] = inputs.pop(0)

                        if self.trace:
                            print(f"[{trace_i}] INPUT {self.memory[dest]} --> {dest}")

            # Opcode 4 outputs the value of its only parameter. For example,
            # the instruction 4,50 would output the value at address 50.
            elif opcode == 4:
                value = self._get_parameter()

                # Provided inputs implies silent output (non-interactive mode)
                if inputs is None:
                    print(f'OUTPUT: {value}')

                if self.trace:
                    print(f"[{trace_i}] OUTPUT {value}")

                self.outputs.append(value)

            # Opcode 5 is jump-if-true: if the first parameter is non-zero,
            # it sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
            elif opcode == 5:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()

                if self.trace:
                    print(f"[{trace_i}] JUMP-IF-TRUE {parameter1} -> {parameter2}")
                if parameter1 != 0:
                    if self.trace:
                        print(f"[{trace_i}] JUMPED -> {parameter2}")
                    self.i = parameter2

            # Opcode 6 is jump-if-false: if the first parameter is zero,
            # it sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
            elif opcode == 6:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()

                if self.trace:
                    print(f"[{trace_i}] JUMP-IF-FALSE {parameter1} -> {parameter2}")
                if parameter1 == 0:
                    if self.trace:
                        print(f"[{trace_i}] JUMPED -> {parameter2}")
                    self.i = parameter2

            # Opcode 7 is less than: if the first parameter is less than the
            # second parameter, it stores 1 in the position given by the third
            # parameter. Otherwise, it stores 0.
            elif opcode == 7:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = 1 if parameter1 < parameter2 else 0

                if self.trace:
                    print(f"[{trace_i}] IS-LESS-THAN {parameter1} < {parameter2} = {self.memory[dest]} --> {dest}")

            # Opcode 8 is equals: if the first parameter is equal to the second
            # parameter, it stores 1 in the position given by the third parameter.
            # Otherwise, it stores 0.
            elif opcode == 8:
                parameter1 = self._get_parameter()
                parameter2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.memory[dest] = 1 if parameter1 == parameter2 else 0

                if self.trace:
                    print(f"[{trace_i}] IS-EQUAL {parameter1} == {parameter2} = {self.memory[dest]} --> {dest}")

            # Opcode 9 adjusts the relative base by the value of its only parameter.
            # The relative base increases (or decreases, if the value is negative) by
            # the value of the parameter.
            elif opcode == 9:
                parameter1 = self._get_parameter()

                if self.trace:
                    print(f"[{trace_i}] RELBASE-CHANGE {parameter1} --> {self._relative_base + parameter1}")
                self._relative_base += parameter1

            # Terminate
            elif opcode == 99:
                self.state = State.HALT

            # Invalid Opcode
            else:
                raise Exception(f'Invalid Opcode: {opcode}')

        return self.outputs if self.state == State.HALT else None

    def get_outputs(self):
        return list(self.outputs)
    
    def clear_outputs(self):
        self.outputs = []

    def get_state(self):
        return self.state