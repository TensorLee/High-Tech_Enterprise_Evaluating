import numpy as np
# import sys
import copy
# from fractions import *
import csv
import os

def oneLine(i, string):
    row = input("请输入判断矩阵上三角第%d行:"% (i+1) + " " + " ".join(string[i][0: i+1]) + " ")
    temp = row.strip().split(' ')
    return temp

def judgementMatrix(n):
    RI = np.array([0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51], dtype=float)
    string = [['1'] * n for _ in range(n)]
    final = [[1] * n for _ in range(n)]

    for i in range(n-1):
        # print(" ".join(string[i][0: i+1]))
        # row = input("请输入判断矩阵上三角第%d行:"% (i+1) + " " + " ".join(string[i][0: i+1]) + " ")
        # temp = row.strip().split(' ')
        temp = oneLine(i, string)
        while len(temp) != (n-i-1):
            print("您输入的元素个数有误，请重新输入：")
            temp = oneLine(i, string)

        string[i][i+1: n] = temp

        for j in range(i+1, n):
            if string[i][j] == '1':
                string[j][i] = '1'

            elif '/' in string[i][j]:
                x = string[i][j].split('/')
                string[j][i] = x[1]

            else:
                string[j][i] = "1" + "/" + string[i][j]
            # print(string, type(string))

    # transfer str values of "string" matrix to float matrix "final"
    for i in range(n):
        for j in range(n):
            if '/' in string[i][j]:
                x = string[i][j].split('/')
                final[i][j] = float(x[0]) / float(x[1])
            else:
                final[i][j] = float(string[i][j])
    # print(final, type(final[0][0]))


    A = np.array(final, dtype=float)
    # print("您输入的判断矩阵为：", A)
    W = copy.deepcopy(A)
    columnSum = np.sum(W, axis=0)
    for i in range(n):
        for j in range(n):
            W[i][j] /= columnSum[j]
    # print(W)
    W = np.sum(W, axis=1, keepdims=True)
    # print(W)
    # print(W.shape)
    sumW = np.sum(W, axis=0)[0]
    # print(sum, type(sum))
    for i in range(n):
        W[i] /= sumW
    # print(W)
    numerator = np.dot(A, W)
    # print(A, W)
    # print(numerator)
    maxEigenvalue = 0
    for i in range(n):
        maxEigenvalue += float(numerator[i] / (n*W[i]))
    # print("最大特征值为：" + str(maxEigenvalue))
    CI = (maxEigenvalue - n) / (n-1)
    if CI <= 0:
        return 0, CI, W
    else:
        CR = CI / RI[n-1]
        if CR < 0.1:
            return 1, CR, W
        else:
            return 2, CI, CR

if __name__ == '__main__':

    print("请输入层次分析判断矩阵A3（5 x 5维度，对角线为1，对称元素互为倒数，以空格分隔）")
    flag, X, Y = judgementMatrix(5)
    while flag == 2:
        print("您输入的判断矩阵不具有一致性，存在矛盾之处，请重新输入：")
        print("请输入层次分析判断矩阵A3（5 x 5维度，对角线为1，对称元素互为倒数，以空格分隔）")        
        flag, X, Y = judgementMatrix(5)
    print("您输入的判断矩阵具有一致性，权重W为：")
    W = list(Y.T)
    print(W, type(W), '\r\n')

    with open("classify_weights.csv", "w", newline='') as result:
        writer = csv.writer(result)
        writer.writerows(W)
    print("权重构造成功！已写入当前文件夹下的 classify_weights.csv \r\n")
    os.system("pause")