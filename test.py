from multiprocessing import Pool, TimeoutError
import time
import os
from multiprocessing import Process, Queue

class My_Pool:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.queue = Queue()
        self.processes = []

    def map(self, func, iterable):
        # Create worker processes
        for i in range(self.num_processes):
            process = Process(target=self._worker, args=(func, self.queue))
            process.start()
            self.processes.append(process)

        # Add items to the queue
        for item in iterable:
            self.queue.put(item)

        # Add sentinels to indicate end of data
        for i in range(self.num_processes):
            self.queue.put(None)

        # Wait for worker processes to finish
        for process in self.processes:
            process.join()

    def _worker(self, func, queue):
        while True:
            item = queue.get()
            if item is None:
                break
            func(item)

def f(x):
    return x*x


if __name__ == '__main__':
    pool = My_Pool(4) # start 4 worker processes
    pool.map(f, range(10))# print "[0, 1, 4,..., 81]"
