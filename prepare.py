import csv
import numpy as np

def read_x():
    with open("x2.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        prepare, name = [], []
        count = -1
        for line in reader:
            if count == -1:
                count += 1
                continue

            for i in range(4):
                if not line[i]:
                    line[i] = "空缺"
            name.append(line[0:4])

            for i in range(4, len(line)):
                if not line[i]:
                    line[i] = 0
            prepare.append(line[4:])

            length = len(line)
            for i in range(length - 4):
                if not prepare[count][i]:
                    prepare[count][i] = 0
                else:
                    prepare[count][i] = float(prepare[count][i])
            count += 1
    prepare = np.array(prepare, dtype = float)
    # print(prepare, type(prepare), prepare.dtype, prepare.shape)
    # print(count, name, type(name))

    x2 = [[0]*17 for _ in range(count)]
    x2 = np.array(x2, dtype=float)
    x2[:, 0] = prepare[:, 1]
    x2[:, 1] = prepare[:, 1] / prepare[:, 0]
    x2[:, 2] = prepare[:, 2]
    x2[:, 3] = prepare[:, 2] / prepare[:, 0]
    x2[:, 4] = prepare[:, 3]
    x2[:, 5] = prepare[:, 3] / prepare[:, 0]
    x2[:, 6] = prepare[:, 4] / prepare[:, 5]
    x2[:, 7] = prepare[:, 5] / prepare[:, 0]
    x2[:, 8] = prepare[:, 6]
    x2[:, 9] = prepare[:, 5] / prepare[:, 3]
    x2[:, 10] = prepare[:, 8]
    x2[:, 11] = prepare[:, 9]
    x2[:, 12] = prepare[:, 10]
    x2[:, 13] = (prepare[:, 9]-prepare[:, 11]) / prepare[:, 9]
    x2[:, 14] = (prepare[:, 10]-prepare[:, 12]) / prepare[:, 10]
    x2[:, 15] = (prepare[:, 7]-prepare[:, 13]) / prepare[:, 7]
    x2[:, 16] = (prepare[:, 8]-prepare[:, 14]) / prepare[:, 8]

    # print(x1, type(x1), x1.dtype, x1.shape)

    # with open("x2_temp.csv", "w", newline='') as temp:
    #     writer = csv.writer(temp)
    #     writer.writerows(x2)

    return x2, count, name
    
if __name__ == '__main__':
    read_x()