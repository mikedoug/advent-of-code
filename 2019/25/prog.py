import itertools
import copy
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

program = computer.Computer(code)

commands = [
    'east',
    'take antenna',
    'west',
    'north',
    'take weather machine',
    'north',
    'take klein bottle',
    'east',                     
    'take spool of cat6',
    'east',                
    'north',
    # 'take infinite loop', 
    'west',
    # 'take giant electromagnet',
    'west',
    # 'take escape pod',
    'east',
    'north',
    'take cake',
    'south',
    'east',
    'east',
    'north',
    # 'take molten lava',
    'north',
    'take tambourine',
    'south',
    'south',
    'south',
    'take shell',
    'east',
    'south',
    # 'take photons',
    'north',
    'west',
    'north',
    'west',
    'south',
    'south',
    'take mug',
    'north',
    'west',
    'south',
    'south',
    'drop shell',
    'drop klein bottle',
    'drop tambourine',
    'drop cake',
    'east'
]

inventory = [
    'shell',
    'klein bottle',
    'tambourine',
    'cake',

    'weather machine',
    'mug',
    'antenna',
    'spool of cat6',
]

command = []
while True:
    program.execute(command)
    print(''.join([chr(x) for x in program.get_outputs()]))
    program.clear_outputs()
    typed = input()
    if typed == '' and len(commands) > 0:
        typed = commands.pop(0)
        print(f'\u001b[31m========> {typed}\u001b[0m')

    command = [ord(x) for x in typed] + [10]

    print (command)