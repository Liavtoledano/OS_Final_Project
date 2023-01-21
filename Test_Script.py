import threading

# shared resource
counter = 0

# create a semaphore with initial value of 0
semaphore = threading.Semaphore(0)

def increment_counter():
    global counter
    for i in range(10):
        counter += 1
        print("Increment: ", counter)
    semaphore.release()

def decrement_counter():
    global counter
    semaphore.acquire()
    for i in range(10):
        counter -= 1
        print("Decrement: ", counter)

# start two threads
t1 = threading.Thread(target=increment_counter)
t2 = threading.Thread(target=decrement_counter)
t1.start()
t2.start()

t1.join()
t2.join()

print("Final value of counter: ", counter)




===> binary video
===> binary image (frame)
===> thread1 = frame1
===> thread2 = frame2 ==> (i,j) ==>

queue (frame1, frame2, frame3, ...... , frameN)

                                         thread1 ->
vid ->   thread     ->   queue  ---->    thread2 ->   -->  result_list
                                         thread3 ->



global list[(0,0), (0,0)]





















