from multiprocessing import JoinableQueue, Lock
import numpy as np
import threading


def find_matrices(frames_queue, write_lock):
    # # Calculate the average value of the bytes
    # avg = np.mean(frame)
    # # Calculate the lower and upper bounds of the range
    # mul_avg = 1.3 * avg
    # # Calculate the lower and upper bounds of the range
    # lower_bound = mul_avg - (mul_avg * 0.05)
    # upper_bound = mul_avg + (mul_avg * 0.05)
    # # Iterate over each index in the data
    # for i in range(frame.shape[0] - 2):
    #     for j in range(frame.shape[1] - 2):
    #         matrix = frame[i:i + 3, j:j + 3]
    #         if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
    #             # Append the middle index of the matrix to the queue
    #             queue_lock.acquire()
    #             matrices_queue.put((i + 1, j + 1))
    #             queue_lock.release()
    while True:
        frame = frames_queue.get()
        if frame == "##END##":
            break
        avg = np.mean(frame)
        # Calculate the lower and upper bounds of the range
        mul_avg = 1.3 * avg
        # Calculate the lower and upper bounds of the range
        lower_bound = mul_avg - (mul_avg * 0.05)
        upper_bound = mul_avg + (mul_avg * 0.05)
        # Iterate over each index in the data
        for i in range(frame.shape[0] - 2):
            for j in range(frame.shape[1] - 2):
                matrix = frame[i:i + 3, j:j + 3]
                if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
                    indexes = (i+1, j+1)
                    with write_lock:
                        print(indexes)




def write_data(matrices_queue):
    with open("output.txt", "w") as file:
        while True:
            matrix = matrices_queue.get()
            if matrix is None:
                break
            file.write(str(matrix) + '\n')
            matrices_queue.task_done()


if __name__ == "__main__":
    num_of_threads = int(input("Enter the number of threads you want to use: "))
    threads = []
    frames_queue = JoinableQueue()
    write_lock = Lock()
    file = open('data\\data\\fr1.bin', 'rb')
    for i in range(num_of_threads):
        t = threading.Thread(target=find_matrices, args= (frames_queue, write_lock))
        t.start()
        threads.append(t)

    bytes_to_read = 600 * 800
    while True:
        data = file.read(bytes_to_read)
        if data == 0:
            break
        data = np.frombuffer(data, dtype=np.uint8).reshape(600, 800)
        frames_queue.put(data)
    file.close()

    for i in range(num_of_threads):
        frames_queue.put("##END##")

    for t in threads:
        t.join()



