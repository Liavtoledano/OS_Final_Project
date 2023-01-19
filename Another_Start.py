from multiprocessing import JoinableQueue
import numpy as np
import threading


def find_matrices(frame, matrices_queue, queue_lock):
    # Calculate the average value of the bytes
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
                # Append the middle index of the matrix to the queue
                queue_lock.acquire()
                matrices_queue.put((i + 1, j + 1))
                queue_lock.release()


def write_data(matrices_queue):
    with open("output.txt", "w") as file:
        while True:
            matrix = matrices_queue.get()
            if matrix is None:
                break
            file.write(str(matrix) + '\n')
            matrices_queue.task_done()


if __name__ == "__main__":
    with open('data\\data\\fr1.bin', 'rb') as file:
        data = file.read()
        num_of_frames = len(data) // (600 * 800)
        data = np.frombuffer(data, dtype=np.uint8).reshape(num_of_frames, 600, 800)

        matrices_queue = JoinableQueue()
        num_of_threads = int(input("Enter the number of threads you want to use: "))

        writer = threading.Thread(target=write_data, args=(matrices_queue,))
        writer.start()
        threads = []

        queue_lock = threading.Lock()

        # for i in range(0, num_of_frames, num_of_threads):
        #     for j in range(num_of_threads):
        #         if i+j >= num_of_frames:
        #             break
        #         frame = data[i+j, :, :]
        #         t = threading.Thread(target=find_matrices, args=(frame, matrices_queue))
        #         t.start()
        #         threads.append(t)

        for i in range(0, num_of_frames, num_of_threads):
            for j in range(num_of_threads):
                if i + j >= num_of_frames:
                    break
                frame = data[i + j, :, :]
                t = threading.Thread(target=find_matrices, args=(frame, matrices_queue, queue_lock,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                print(threading.active_count())



        matrices_queue.join()
        matrices_queue.put(None)
        writer.join()
