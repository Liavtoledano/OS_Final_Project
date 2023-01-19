import time
from queue import Queue
from threading import Thread, current_thread

que = Queue()


def run_producer():
    print("I am the producer")
    for i in range(20):
        item = "packet_" + str(i)  # producing an item
        que.put(item)
        time.sleep(1.0)


def run_consumer():
    print("I am a consumer", current_thread().name)
    while True:
        item = que.get()
        print(current_thread().name, "got", item)
        time.sleep(5)


for i in range(10):  # Starting 10 consumers !
    t = Thread(target=run_consumer)
    t.start()

run_producer()
