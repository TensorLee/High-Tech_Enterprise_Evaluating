import matrix
# from dist import matrix
import csv
import numpy as np
import os
import traceback
from prepare import read_x

def compute(n, x):
    mean = np.mean(x, axis = 0)
    std = np.std(x, axis=0)
    # print("各项指标均值mean为：")
    # print(mean, type(mean), mean.dtype, mean.shape, '\r\n')
    # print("各项指标标准差std为：")
    # print(std, type(std), std.dtype, std.shape, '\r\n')
    I = [-1 for _ in range(len(mean))]
    I = np.array(I, dtype=float)
    for i in range(37):
        if mean[i] == 0:
            I[i] = 0
        else: I[i] = std[i] / mean[i]
    # print("各项指标变异系数为：")
    # print(I, type(I), I.dtype, I.shape, '\r\n')
    sumI = np.sum(I)
    # print(sumI, type(sumI))
    for i in range(37):
        I[i] /= sumI
    # print("各项指标变异系数权重I为：")
    # print(I, type(I), I.dtype, I.shape, '\r\n')
    for j in range(37):
        if std[j] == 0: continue
        for i in range(n):
            x[i, j] = (x[i, j] - mean[j]) / std[j]
    # print("无量纲化（标准化）后的企业数据x为：")
    # print(x, type(x), x.dtype, x.shape, '\r\n')
    return I, x

def read_Weights():
    with open("comprehensive_weights.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for line in reader:
            if count == 0:
                W = line
            if count == 1:
                N = line
            if count == 2:
                O = line
            if count == 3:
                R = line
            if count == 4:
                V = line
            if count == 5:
                K = line
            count += 1
    # print(W, type(W), type(W[0]), W[0])
    W = np.array(W, dtype = float)
    N = np.array(N, dtype = float)
    O = np.array(O, dtype = float)
    R = np.array(R, dtype = float)
    V = np.array(V, dtype = float)
    K = np.array(K, dtype = float)

    return W, N, O, R, V, K

if __name__ == '__main__':
    try:
        Weights = [-1 for _ in range(37)]

        # print("变异系数权重为：")
        # print(I, type(I), I.dtype, I.shape)

        # write_x()
        x, n, name = read_x()
        # print("导入的企业数据x为：")
        # print(x, type(x), x.dtype, x.shape, '\r\n')

        I, x = compute(n, x)
        W, N, O, R, V, K = read_Weights()

        for i in range(0, 3):
            Weights[i] = I[i] * V[0] * N[0] * W[0]
        for i in range(3, 6):
            Weights[i] = I[i] * V[1] * N[0] * W[0]
        for i in range(6, 13):
            Weights[i] = I[i] * N[1] * W[0]
        for i in range(13, 19):
            Weights[i] = I[i] * K[0] * O[0] * W[1]
        for i in range(19, 23):
            Weights[i] = I[i] * K[1] * O[0] * W[1]
        for i in range(23, 28):
            Weights[i] = I[i] * O[1] * W[1]
        for i in range(28, 31):
            Weights[i] = I[i] * R[0] * W[2]
        for i in range(31, 35):
            Weights[i] = I[i] * R[1] * W[2]
        for i in range(35, 37):
            Weights[i] = I[i] * R[2] * W[2]

        Weights = np.array(Weights, dtype=float)
        # print("最终权重Weights为：")
        # print(Weights, type(Weights), Weights.dtype, Weights.shape, '\r\n')

        res = [[0]*4 for _ in range(n)]
        for i in range(n):
            res[i][0] = np.dot(x[i][0:13], Weights[0:13])
            res[i][1] = np.dot(x[i][13:28], Weights[13:28])
            res[i][2] = np.dot(x[i][28:37], Weights[28:37])
            res[i][3] = res[i][0] + res[i][1] + res[i][2]
            # res[i][4] = np.dot(x[i], Weights)
        # print("企业综合指标计算成功，结果为：")
        # print(res, type(res), '\r\n')
        with open("comprehensive_result.csv", "w", newline='') as result:
            writer = csv.writer(result)
            writer.writerow(["ORG_NAME", "STAT_YEAR", "GXJSQY_TECH_NAME", "QYMC", "SC_YFGXD", "SC_ZYNL", "SC_QYCZSD", "SC_ZHPF"])
            for i in range(n):
                writer.writerow((name[i] + res[i]))
        print("企业综合指标计算成功！结果已写入当前文件夹下的 comprehensive_result.csv")


    except FileNotFoundError:
        print("comprehensive_weights.csv 或 x1.csv不存在，请先构造它们。")

    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        os.system("pause")