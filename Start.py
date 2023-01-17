import byte_func
import numpy as np



if __name__ == "__main__":
    # file = open("data\\data\\fr0.bin", "rb")
    # image_size = 600*800
    # byte = file.read(1)
    # cnt = 0
    # summ = 0
    # for line in file:
    #     for byte in line:
    #         summ += byte
    #
    # avg = summ/image_size
    # print(avg)
    # file.close()

    with open('data\\data\\fr0.bin', 'rb') as file:
        # Read the contents of the file into a variable
        data = file.read()
        # Convert the data to a numpy array
        data = np.frombuffer(data, dtype=np.uint8)
        # reshape the data to 600x800
        data = data.reshape(600, 800)
        # Calculate the average value of the bytes
        avg = np.mean(data)
        mul_avg = 1.3 * avg
        # Calculate the lower and upper bounds of the range
        lower_bound = mul_avg - (mul_avg * 0.05)
        upper_bound = mul_avg + (mul_avg * 0.05)
        # Initialize a variable to store the 3x3 matrices
        matrices = []
        indexes = []
        # Iterate over each index in the data
        for i in range(data.shape[0] - 2):
            for j in range(data.shape[1] - 2):
                matrix = data[i:i + 3, j:j + 3]
                if np.all(lower_bound <= matrix) and np.all(matrix <= upper_bound):
                    matrices.append(matrix)
                    # save the middle indexes of the matrix
                    indexes.append((i + 1, j + 1))
        # Print the 3x3 matrices that are within the range
        print("3x3 matrices within the range:", matrices)
        print(indexes)