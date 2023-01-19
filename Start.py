import numpy as np
from threading import Thread, Lock
import matplotlib.pyplot as plt


# Define the function to find the matrices
def find_matrices(frame, lock):
    # Calculate the average value of the bytes
    avg = np.mean(frame)
    mul_avg = 1.3 * avg
    # Calculate the lower and upper bounds of the range
    lower_bound = mul_avg - (mul_avg * 0.05)
    upper_bound = mul_avg + (mul_avg * 0.05)
    # Initialize a variable to store the 3x3 matrices
    matrices = []
    idx = []
    # Iterate over each index in the data
    for i in range(frame.shape[0] - 2):
        for j in range(frame.shape[1] - 2):
            matrix = frame[i:i + 3, j:j + 3]
            if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
                lock.acquire()
                matrices.append(matrix)
                idx.append((str(j + 1), str(i + 1)))
                lock.release()
    return idx[-1]


def write_to_output_file(file_name, data):
    with open(file_name, "w") as output:
        output.write(data)
        output.write("\n")


if __name__ == "__main__":
    NUM = ["0", "1", "2"]
    files_names = ['fr' + num + '.bin' for num in NUM]
    commands_files = ['command_' + num + '.txt' for num in NUM]
    for idx in range(len(files_names)):
        # Open the video file in read mode
        full_path_to_file = 'data\\data\\' + files_names[idx]
        all_idx = []
        with open(full_path_to_file, 'rb') as file:
            # Read the contents of the file into a variable
            data = file.read()
            # Get the number of frames
            num_of_frames = len(data) // (600 * 800)
            # reshape the data to 600x800xnum_of_frames
            data = np.frombuffer(data, dtype=np.uint8).reshape(num_of_frames, 600, 800)
            # Initialize a variable to store the 3x3 matrices for all frames
            all_matrices = []

            lock = Lock()
            threads = []
            writer = Thread(target=write_to_output_file, args=(all_idx,))
            writer.start()
            for i in range(num_of_frames):
                frame = data[i, :, :]
                t = Thread(target=find_matrices, args=frame)
                t.start()
                threads.append(t)
                # result = find_matrices(frame)
                # all_matrices.append(result[0])
                all_idx.append(find_matrices(frame))

                # write result to output file
                # with open(commands_files[idx], 'a') as output:
                #     output.write(str(i) + ": ")
                #     output.write(all_idx[-1][1]+ " " + all_idx[-1][0])
                #     output.write("\n")

                # plt.imshow(frame, cmap='gray')
                # plt.scatter(result[1][0][0], result[1][0][1], color="red")
                # plt.show()
            # Print the 3x3 matrices that are within the range for all frames
            # print("3x3 matrices within the range for all frames:", all_matrices)
