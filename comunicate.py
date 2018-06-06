import os, time
import threading, queue
import multiprocessing


# class SenderThread(threading.Thread):
#     def __init__(self, value_queue, inputs):
#         super(SenderThread, self).__init__()
#         self.value_queue = value_queue
#         self.stoprequest = threading.Event()
#         self.inputs = inputs
#         self.value = 0

#     def run(self):
#         while not self.stoprequest.isSet():
#             self.value += 1
#             self.value_queue.put(self.value)
#             self.inputs.add(self.value)
#             print(self.value)
#             if self.value > 10:
#                self.stoprequest.set()

#     def join(self, timeout=None):
#         self.stoprequest.set()
#         super(SenderThread, self).join(timeout)

class WorkerThread(threading.Thread):

    def __init__(self, value_queue, result_q):
        super(WorkerThread, self).__init__()
        self.value_queue = value_queue
        self.value = 5
        self.result_q = result_q
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
                self.value = self.value_queue.get(True, 0.05)
                self.result_q.put((self.value, self.compute_something_huge(self.value)))
            except queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)

    def compute_something_huge(self, i):
        time.sleep(1)
        return i/2.0

def main(args):
    # Create a single input and a single output queue for all threads.
    value_queue = queue.Queue()
    for i in range(30):
        value_queue.put(i)
    result_q = queue.Queue()

    # Create the "thread pool"
    pool = [WorkerThread(value_queue=value_queue, result_q=result_q) for _ in range(multiprocessing.cpu_count())]

    # Start all threads
    for thread in pool:
        thread.start()

    values = set()

    #mySender = SenderThread(value_queue=value_queue, inputs=values)
    #mySender.start()

    # Give the workers some work to do
    while not value_queue.empty():
        a,b = result_q.get()
        print(a,b)
        if b not in values:
            value_queue.put(b)

    # Ask threads to die and wait for them to do it
    #mySender.join()
    for thread in pool:
        thread.join()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

