class Decompile(object):
    def __init__(self, memory):
        # We always copy the passed-in memory so that we never harm the caller
        self.memory = list(memory)
        self._i = 0

    def _next_instruction(self):
        instruction = self.memory[self._i]
        modes, opcode = divmod(instruction, 100)
        modes = [int(x) for x in reversed(str(modes))]

        self._parameter_modes = modes
        self._i += 1

        return opcode

    def _next_mode(self):
        if len(self._parameter_modes) > 0:
            return self._parameter_modes.pop(0)
        return 0

    def _get_parameter(self):
        value = self.memory[self._i]
        self.output[self._i] = ''
        mode = self._next_mode()
        self._i += 1

        if mode == 0: # Positional
            return f'@{value}'
        elif mode == 1: # Immediate
            return f'{value}'
        elif mode == 2: # Relative
            return f'R{value}'
        else:
            raise Exception(f"Invalid Mode: {mode}")

    def _get_dest_parameter(self):
        value = self.memory[self._i]
        self.output[self._i] = ''
        mode = self._next_mode() # Throw away
        self._i += 1

        if mode == 0: # Positional
            return f'@{value}'
        elif mode == 1: # Immediate
            raise Exception(f"Mode for get dest parameter {mode}")
        elif mode == 2: # Relative
            return f'R{value}'
        else:
            raise Exception(f"Invalid Mode: {mode}")

    def decompile(self):
        self.jumplist = [0]
        self.output = [None for i in self.memory]

        while len(self.jumplist) > 0:
            self._i = self.jumplist.pop()

            if self.output[self._i] is None:
                self.do_chunk()

        for i in range(len(self.output)):
            if self.output[i] is None:
                self.output[i] = f'{i:10} {"DATA":8} {self.memory[i]}'
    
    def do_chunk(self):
        last_const_to_R0 = None
        while self._i < len(self.memory):
            trace_i = self._i
            opcode = self._next_instruction()

            # ADD
            if opcode == 1:
                p1 = self._get_parameter()
                p2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.output[trace_i] = f'{trace_i:10} {"ADD":8} {p1} {p2} {dest}'

                last_const_to_R0 = None
                try:
                    if dest == 'R0':
                        last_const_to_R0 = int(p1) + int(p2)
                except:
                    pass

            # MULTIPLY
            elif opcode == 2:
                p1 = self._get_parameter()
                p2 = self._get_parameter()
                dest = self._get_dest_parameter()

                self.output[trace_i] = f'{trace_i:10} {"MUL":8} {p1} {p2} {dest}'

                last_const_to_R0 = None
                try:
                    if dest == 'R0':
                        last_const_to_R0 = int(p1) * int(p2)
                except:
                    pass

            # Opcode 3 takes a single integer as input and saves it to the
            # address given by its only parameter. For example, the
            # instruction 3,50 would take an input value and store it at
            # address 50.
            elif opcode == 3:
                dest = self._get_dest_parameter()
                self.output[trace_i] = f'{trace_i:10} {"INPUT":8} {dest}'
                last_const_to_R0 = None

            # Opcode 4 outputs the value of its only parameter. For example,
            # the instruction 4,50 would output the value at address 50.
            elif opcode == 4:
                value = self._get_parameter()
                self.output[trace_i] = f'{trace_i:10} {"OUTPUT":8} {value}'
                last_const_to_R0 = None

            # Opcode 5 is jump-if-true: if the first parameter is non-zero,
            # it sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
            elif opcode == 5:
                p1 = self._get_parameter()
                p2 = self._get_parameter()
                self.output[trace_i] = f'{trace_i:10} {"JUMP-IF":8} {p1} {p2}'
                if last_const_to_R0 is not None:
                    self.jumplist.append(last_const_to_R0)
                last_const_to_R0 = None

                try:
                    self.jumplist.append(int(p2))
                except:
                    print(f'Invalid jump destination {p2}')
                try:
                    if int(p1) != 0:
                        self.output[trace_i] += '\n'
                        return
                except:
                    pass

            # Opcode 6 is jump-if-false: if the first parameter is zero,
            # it sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
            elif opcode == 6:
                p1 = self._get_parameter()
                p2 = self._get_parameter()
                self.output[trace_i] = f'{trace_i:10} {"JUMP-IF!":8} {p1} {p2}'
                if last_const_to_R0 is not None:
                    self.jumplist.append(last_const_to_R0)
                last_const_to_R0 = None

                try:
                    self.jumplist.append(int(p2))
                except:
                    print(f'Invalid jump destination {p2}')
                try:
                    if int(p1) == 0:
                        self.output[trace_i] += '\n'
                        return
                except:
                    pass


            # Opcode 7 is less than: if the first parameter is less than the
            # second parameter, it stores 1 in the position given by the third
            # parameter. Otherwise, it stores 0.
            elif opcode == 7:
                p1 = self._get_parameter()
                p2 = self._get_parameter()
                dest = self._get_dest_parameter()
                self.output[trace_i] = f'{trace_i:10} {"LESSTHAN":8} {p1} {p2} {dest}'
                last_const_to_R0 = None

            # Opcode 8 is equals: if the first parameter is equal to the second
            # parameter, it stores 1 in the position given by the third parameter.
            # Otherwise, it stores 0.
            elif opcode == 8:
                p1 = self._get_parameter()
                p2 = self._get_parameter()
                dest = self._get_dest_parameter()
                self.output[trace_i] = f'{trace_i:10} {"EQUALS":8} {p1} {p2} {dest}'
                last_const_to_R0 = None

            # Opcode 9 adjusts the relative base by the value of its only parameter.
            # The relative base increases (or decreases, if the value is negative) by
            # the value of the parameter.
            elif opcode == 9:
                p1 = self._get_parameter()
                self.output[trace_i] = f'{trace_i:10} {"REL-ADD":8} {p1}'
                last_const_to_R0 = None

            # Terminate
            elif opcode == 99:
                self.output[trace_i] = f'{trace_i:10} {"HALT":8}\n'
                return

            # Invalid Opcode
            else:
                raise Exception(f'Invalid Opcode: {opcode}')

if __name__ == '__main__':
    import sys

    code = [int(x) for x in sys.stdin.readline().rstrip().split(',')]
    decompiler = Decompile(code)
    decompiler.decompile()

    print("------------------")
    print("\n".join([x for x in decompiler.output if x is not None and x != '']))
    print("------------------")
