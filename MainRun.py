from threading import Thread, Lock
import time
from multiprocessing import JoinableQueue
import numpy as np

# in order to keep frames in the right order, this global list will be initiated for each frame as (0,0).
# results = [(0,0) x num_of_frames]
# when an object will be found in the n frame, this list will be updated in the n index with the values.
# for example: if there are 3 frames only and object was found in x,y location in the 2nd frame before 1st frame
# location found ===> result = [(0,0), (x,y), (0,0)].

results = []


def write_to_output(output_file):
    i = 0  # index to indicate the next element to print.
    with open(output_file, "w") as output:
        while True:
            if not results:  # result in []
                continue
            else:
                try:
                    if results[i] == "###END###":  # end indication
                        break
                except:
                    continue

            if results[i] == (0, 0):
                # the 'i' indicates the next frame to print.
                # if the 'i' frame is still not analyzed, wait for it to be analyzed.
                continue
            else:
                # the 'i' frame is analyzed and ready to be printed.
                output.write(str(i) + ": " + str(results[i][0]) + " " + str(results[i][1]))
                output.write("\n")
                i += 1
            time.sleep(0.01)


def read_frames(path_to_file, queue, num_of_threads, lock):
    # no need for lock because only 1 thread is working on the file
    with open(path_to_file, "rb") as video:
        frame_num = 0
        while True:
            # read 600 * 800 bytes from the video
            frame = video.read(600 * 800)
            # if reached end, break
            if frame == b'':
                break
            # reshape it to be 600 * 800 frame
            frame = np.frombuffer(frame, dtype=np.uint8).reshape(600, 800)
            # put in the queue the frame and the frame number
            queue.put((frame, frame_num))
            frame_num += 1
            # add to results list (0,0) in the frame index
            global results
            with lock:
                # lock access to results global variable.
                results.append((0, 0))
            time.sleep(0.03)

    # after breaking, put ("###END###", "###END###") for each working thread to mark end of processing.
    for _ in range(num_of_threads):
        queue.put(("###END###", "###END###"))


def find_matrix(queue, lock):
    # Find 3*3 matrix which all of its values are in the range of the (average * 1.3) +-5%
    while True:
        task = queue.get()
        frame_num = task[1]
        frame = task[0]
        if frame == "###END###":    # end indication
            with lock:
                results.append("###END###")
            break
        # avg of frame
        average = np.mean(frame)
        # avg - 5%
        lower_bound = average * 1.3 * 0.95
        # avg + 5%
        upper_bound = average * 1.3 * 1.05
        # added this flag because in frame 29 at fr3.bin, no correct object found.
        Found = False
        for i in range(frame.shape[0] - 2):     # -2 for not exceed the frame range with mask
            for j in range(frame.shape[1] - 2):
                # 3x3 matrix with the frame values
                matrix = frame[i:i + 3, j:j + 3]
                # if all values in avg +- 5% range then object is found
                if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
                    queue.task_done()
                    Found = True
                    # lock for only 1 thread have access to global results list.
                    with lock:
                        results[frame_num] = (i + 1, j + 1)

        if not Found:
            # if object is not found in the frame then write "not found" in this frame result.
            queue.task_done()
            # lock for only 1 thread have access to global results list.
            with lock:
                results[frame_num] = ("not found", "not found")
        time.sleep(0.01)


def main():
    NUM = ["0", "1", "2", "3"]
    files_names = ['fr' + num + '.bin' for num in NUM]
    commands_files = ['command_' + num + '.txt' for num in NUM]
    num_of_threads = int(input("please enter the number of threads to work with: "))

    for idx in range(len(files_names)):
        path_to_file = files_names[idx]

        start = time.time()

        # global variable lock to lock access to it.
        results_lock = Lock()

        ### reading the frames from the video ###
        queue = JoinableQueue()     # queue for results and frame numbers.
        read_thread = Thread(target=read_frames, args=(path_to_file, queue, num_of_threads, results_lock))
        read_thread.start()

        ### writing the results to an output file ###
        write_thread = Thread(target=write_to_output, args=(commands_files[idx],))
        write_thread.start()

        # save analyzing threads to join them.
        analyze_threads = []

        # create analyzing threads.
        for i in range(num_of_threads):
            t = Thread(target=find_matrix, args=(queue, results_lock))
            analyze_threads.append(t)
            t.start()

        # join read thread.
        read_thread.join()

        # join analyzing threads.
        for t in analyze_threads:
            t.join()

        # wait for all tasks to be done.
        queue.join()

        # join write thread.
        write_thread.join()

        end = time.time()
        print("finished in: ", end - start)

        # start fresh next video
        global results
        results = []


if __name__ == "__main__":
    main()
