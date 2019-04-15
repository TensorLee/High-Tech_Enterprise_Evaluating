import csv
import numpy as np
import os

def read_y():
    with open("y.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        y, name = [], []
        count = -1
        for line in reader:
            if count == -1:
                count += 1
                continue
            for i in range(4):
                if not line[i]:
                    line[i] = "空缺"
            name.append(line[0: 4])
            for i in range(4, len(line)):
                if not line[i]:
                    line[i] = 0
            y.append(line[4: ])
            count += 1
    y = np.array(y, dtype = float)
    # print(y, type(y), y.dtype, y.shape)
    return y, count, name

if __name__ == '__main__':
    y, n, name = read_y()
    # print(name, type(name))

    a = 0.4
    while True:
        confirm = input("平滑常数a值默认为 0.4，确认请输 y，修改请输 n：")
        if confirm == 'y':
            break
        elif confirm == 'n':
            a = float(input("请输入您想修改的平滑常数a值："))
            if a < 0 or a > 1:
                print("平滑常数a值必须在0到1之间，请重新输入：")
                continue
            break
        else:
            print("您的输入不是 y 或 n，请重新输入。")

    y0s0 = np.sum(y[:, 0:3], axis=1, keepdims=True) / 3
    # print(y0s0, type(y0s0), y0s0.dtype, y0s0.shape)
    y1s0 = np.sum(y[:, 3:6], axis=1, keepdims=True) / 3
    # print(y1s0, type(y1s0), y1s0.dtype, y1s0.shape)
    y2s0 = np.sum(y[:, 6:9], axis=1, keepdims=True) / 3
    # print(y2s0, type(y2s0), y2s0.dtype, y2s0.shape)
    y3s0 = np.sum(y[:, 9:12], axis=1, keepdims=True) / 3
    # print(y3s0, type(y3s0), y3s0.dtype, y3s0.shape)
    # s0 /= 3
    s0 = np.hstack((y0s0, y1s0, y2s0, y3s0))
    # print(s0, type(s0), s0.dtype, s0.shape)

    y0 = np.hstack((y[:,0].reshape(n,1), y[:,3].reshape(n,1), y[:,6].reshape(n,1), y[:,9].reshape(n,1)))
    # print(y0, type(y0), y0.dtype, y0.shape)

    y1 = np.hstack((y[:,1].reshape(n,1), y[:,4].reshape(n,1), y[:,7].reshape(n,1), y[:,10].reshape(n,1)))
    # print(y0, type(y0), y0.dtype, y0.shape)

    y2 = np.hstack((y[:,2].reshape(n,1), y[:,5].reshape(n,1), y[:,8].reshape(n,1), y[:,11].reshape(n,1)))
    # print(y2, type(y2), y2.dtype, y2.shape)

    s1 = a * y0 + (1-a) * s0
    s2 = a * y1 + (1-a) * s1
    s3 = a * y2 + (1-a) * s2
    # print(s3, type(s3), s3.dtype, s3.shape)

    # s1 = a*y[:, 0] + (1-a)*s0
    # s2 = a*y[:, 1] + (1-a)*s1
    # s3 = a*y[:, 2] + (1-a)*s2
    # res = [[0] for _ in range(n)]
    # s3 = np.reshape(s3, (n, 3))
    # s3 = s3.T
    # print(s3, type(s3), s3.dtype, s3.shape)
    # for i in range(n):
    #     res[i][0] = s3[i]
    with open("y_predict.csv", "w", newline='') as csvfile: 
        writer = csv.writer(csvfile)
        #先写入columns_name
        # writer.writerow(["预测下一年"])
        writer.writerow(["ORG_NAME", "STAT_YEAR", "GXJSQY_TECH_NAME", "QYMC", "SC_YFGXD", "SC_ZYNL", "SC_QYCZSD", "SC_ZHPF"])
        #写入多行用writerows
        # res = zip(name, s3)
        # print(res)
        for i in range(n):
            # print(name[i])
            tmp = list(s3[i])
            writer.writerow((name[i] + tmp))
        # writer.writerows(res)
    print("计算成功！预测下一年数据已写入 y_predict.csv")
    os.system("pause")