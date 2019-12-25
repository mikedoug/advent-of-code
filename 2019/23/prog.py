import itertools
import copy
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import threading
import time
import queue

import computer # pylint: disable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

computers = []

class NAT(threading.Thread):
    def __init__(self):
        super().__init__()
        self.value = (None, None)
        self.last_sent = (None, None)

    def set_value(self, x, y):
        self.value = (x, y)

    def run(self):
        print('NAT thread starting')
        while True:
            state = 'IDLE'
            for c in computers:
                if c.idle_count < 5:
                    state = 'BUSY'
                    break
            
            if state == 'IDLE':
                if self.value == (None, None):
                    print('NAT detected IDLE, but no value has been captured...')
                else:
                    print(f'NAT sent {self.value}')
                    computers[0].q.put([self.value[0], self.value[1]])

                    if self.value[1] == self.last_sent[1]:
                        print(f'NAT sent {self.value[1]} twice in a row for y')
                    self.last_sent = self.value

            time.sleep(.01)

natthread = NAT()

class ComputerThread(threading.Thread):
    def __init__(self, i):
        super().__init__()
        self.c = computer.Computer(code)
        self.q = queue.Queue()
        self.i = i
        self.idle_count = 0

    def run(self):

        # print (f'Starting computer {self.i}')
        self.c.execute([self.i])

        iter = 1000
        while iter > 0:
            iter -= 1

            # print(f'{self.i} {c.get_state()}')
            if self.c.get_state() == computer.State.WAIT:
                try:
                    # print(f'{self.i} queue {self.q}')
                    packet = self.q.get(block=True, timeout=.01)
                    # print(f'{self.i} >> Sent {packet}')
                    self.c.execute([packet[0], packet[1]])
                    self.q.task_done()
                except queue.Empty:
                    # print(f'{self.i} >> No Packet')
                    self.c.execute([-1])
                    self.idle_count += 1
            else:
                print(f'{self.i} -- {self.c.get_state()}')

            outputs = self.c.get_outputs()
            if len(outputs) > 0:
                self.idle_count = 0
                self.c.clear_outputs()

                # print(f"{self.i} outputs: {outputs}")
                sys.stdout.flush()

                outputs = [outputs[i:i+3] for i in range(0, len(outputs), 3)]
                for o in outputs:
                    print (i, o[0], o[1], o[2])
                    if o[0] != 255:
                        computers[o[0]].q.put(o[1:3])
                        # print (f'Queued on {o[0]}: {o[1:3]}')
                    else:
                        natthread.set_value(o[1], o[2])

numcomputers = 50
for i in range(numcomputers):
    computers.append(ComputerThread(i))

for i in range(numcomputers):
    computers[i].start()

natthread.start()

for i in range(numcomputers):
    computers[i].join()
natthread.join()