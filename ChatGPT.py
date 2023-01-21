import numpy as np
from threading import Thread
from queue import Queue
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

def process_frame(frame):
    # Find 3*3 matrix which all of its values are in the range of the (average * 1.3) +-5%
    average = np.mean(frame)
    lower_bound = average * 1.3 * 0.95
    upper_bound = average * 1.3 * 1.05
    result = []
    for i in range(frame.shape[0] - 2):
        for j in range(frame.shape[1] - 2):
            matrix = frame[i:i + 3, j:j + 3]
            if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
                result.append((i+1, j+1))
    return result

def save_output(output_file, q):
    with open(output_file, "w") as f:
        while True:
            try:
                i, j = q.get(block=False)
                f.write(f"{i},{j}\n")
            except:
                break

def main():
    # Ask the user the amount of threads he wants to use.
    num_threads = int(input("Enter the number of threads to use: "))
    q = Queue()
    # Open the binary video file and read it frame by frame
    with open("data\\data\\fr1.bin", "rb") as binary_file:
        bytes_to_read = 600*800
        frame_num = 0
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            while True:
                frame_data = binary_file.read(bytes_to_read)
                if not frame_data:
                    break
                frame = np.frombuffer(frame_data, dtype=np.uint8).reshape(600, 800)
                # process the frame using the executor
                result = executor.submit(process_frame, frame)
                for r in result.result():
                    q.put(r)
                frame_num += 1
                # save the output after a certain number of frames
                if frame_num % num_threads == 0:
                    save_thread = Thread(target=save_output, args=("output.txt", q))
                    save_thread.start()
                    save_thread.join()
    # When the while loop is done, start the last save thread and wait for it to finish.
    save_thread = Thread(target=save_output, args=("output.txt", q))
    save_thread.start()
    save_thread.join()

if __name__ == "__main__":
    main()

