from threading import Thread, Lock
import time
from multiprocessing import JoinableQueue
import numpy as np

results = []


def write_to_output():
    i = 0
    # global results
    with open("output2.txt", "w") as output:
        while True:
            if not results:
                continue
            else:
                try:
                    if results[i] == "###END###":
                        break
                except:
                    continue

            if results[i] == (0, 0):
                # print(results)
                continue
            else:
                print("im here")
                output.write(str(i) + ": " + str(results[i][0]) + " " + str(results[i][1]))
                output.write("\n")
                i += 1
            print("current result index is:", i)
            time.sleep(0.01)


def read_frames(queue, num_of_threads):
    with open("data\\data\\fr1.bin", "rb") as video:
        frame_num = 0
        while True:
            frame = video.read(600 * 800)
            if frame == b'':
                break
            frame = np.frombuffer(frame, dtype=np.uint8).reshape(600, 800)
            queue.put((frame, frame_num))
            frame_num += 1
            global results
            results.append((0, 0))
            # 3 fps
            time.sleep(0.03)

    for _ in range(num_of_threads):
        queue.put(("###END###", "###END###"))


def find_matrix(queue, output_file_name, lock, thread_id):
    # Find 3*3 matrix which all of its values are in the range of the (average * 1.3) +-5%
    while True:
        task = queue.get()
        frame_num = task[1]
        frame = task[0]
        if frame == "###END###":
            results.append("###END###")
            break
        average = np.mean(frame)
        lower_bound = average * 1.3 * 0.95
        upper_bound = average * 1.3 * 1.05
        for i in range(frame.shape[0] - 2):
            for j in range(frame.shape[1] - 2):
                matrix = frame[i:i + 3, j:j + 3]
                if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
                    queue.task_done()
                    with lock:
                        results[frame_num] = (i + 1, j + 1)
        time.sleep(0.01)


def main():
    num_of_threads = int(input("please enter the number of threads to work with: "))
    start = time.time()
    ### reading the frames from the video ###
    queue = JoinableQueue()
    read_thread = Thread(target=read_frames, args=(queue, num_of_threads))
    read_thread.start()

    write_thread = Thread(target=write_to_output)
    write_thread.start()

    print_lock = Lock()
    analyze_threads = []

    for i in range(num_of_threads):
        t = Thread(target=find_matrix, args=(queue, "output.txt", print_lock, i))
        analyze_threads.append(t)
        t.start()
    read_thread.join()

    for t in analyze_threads:
        t.join()

    write_thread.join()

    end = time.time()
    print("finished in: ", end - start)
    # for item in results:
    #     print(item)


if __name__ == "__main__":
    main()
