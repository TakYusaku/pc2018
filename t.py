"""
from collections import deque

class Memory:
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self):
        return self.buffer.pop()

    def len(self):
        return len(self.buffer)

memory = Memory(10)
for i in range(10):
    memory.add(i)

for i in range(memory.len()):
    print(memory.sample())
"""
a = 115
print(str(int(a * 0.9 * (-1))))
