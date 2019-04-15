import matrix
import csv
import numpy as np
import os
import traceback
from prepare import read_x

def read_Weights():
    with open("classify_weights.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            W = line
    W = np.array(W, dtype = float)

    return W

def compute(n, x):
    mean = np.mean(x, axis = 0)
    std = np.std(x, axis=0)
    # print("各项指标均值mean为：")
    # print(mean, type(mean), mean.dtype, mean.shape, '\r\n')
    # print("各项指标标准差std为：")
    # print(std, type(std), std.dtype, std.shape, '\r\n')
    I = [-1 for _ in range(len(mean))]
    for i in range(len(mean)):
        if mean[i] == 0:
            I[i] = 0
        else: I[i] = std[i] / mean[i]
    # print("各项指标变异系数为：")
    # print(I, type(I), I.dtype, I.shape, '\r\n')
    sumI = np.sum(I)
    # print(sumI, type(sumI))
    for i in range(17):
        I[i] /= sumI
    # print("各项指标变异系数权重I为：")
    # print(I, type(I), I.dtype, I.shape, '\r\n')
    for j in range(17):
        if std[j] == 0: continue
        for i in range(n):
            x[i, j] = (x[i, j] - mean[j]) / std[j]
    # print("无量纲化（标准化）后的企业数据x为：")
    # print(x, type(x), x.dtype, x.shape, '\r\n')
    return I, x

if __name__ == '__main__':
    try:
        x, n, name = read_x()
        # print("导入的企业数据x为：")
        # print(x, type(x), x.dtype, x.shape, '\r\n')

        I, x = compute(n, x)
        W = read_Weights()

        L = [-1 for _ in range(10)]
        L = np.array(L, dtype = float)
        for i in range(6):
            L[i] = I[i] * W[0]
        for i in range(6, 10):
            L[i] = W[i-5]
        # print("综合权重L为：")
        # print(L, type(L), L.dtype, L.shape, '\r\n')

        res = [[-1]*3 for _ in range(n)]
        # print(res, type(res))
        for i in range(n):
            # tmp = x[i]
            # print(tmp, type(tmp), tmp.dtype, tmp.shape)
            res[i][0] = np.dot(x[i][10:13], I[10:13])
            res[i][1] = np.dot(x[i][13:17], I[13:17])
            res[i][2] = np.dot(x[i][0:10], L[0:10])

        # print("企业归类指标计算成功，结果为：")
        # print(res, type(res), '\r\n')

        with open("classify_result.csv", "w", newline='') as csvfile: 
            writer = csv.writer(csvfile)
            #先写入columns_name
            writer.writerow(["ORG_NAME", "STAT_YEAR", "GXJSQY_TECH_NAME", "QYMC", "SC_QYGM","SC_FZDX","SC_CZSD"])
            #写入多行用writerows
            for i in range(n):
                writer.writerow((name[i] + res[i]))
        print("企业归类指标计算成功！结果已写入当前文件夹下的 classify_result.csv")

    except FileNotFoundError:
        print("classify_weights.csv 或 x2.csv不存在，请先构造它们。")

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        os.system("pause")
    finally:
        os.system("pause")