from sklearn import metrics
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import decimal

import matplotlib.font_manager as fm
def PerformanceMetrics(actual, predict):
    # 计算分类性能矩阵
    # 输入：实际标签和预测标签，输出：分类性能矩阵
    accuracy = metrics.accuracy_score(actual, predict)
    Precision = metrics.precision_score(actual, predict, average='macro')
    Recall = metrics.recall_score(actual, predict, average='macro')
    F1score = metrics.f1_score(actual, predict, average='macro')
    Confusion_Matrix = metrics.confusion_matrix(actual, predict)
    k = kappa(Confusion_Matrix)
    return accuracy, Precision, Recall, F1score, Confusion_Matrix, k

def My_ConfusionMatrix(label_test, label_predict, title):
    # 绘制混淆矩阵：
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

    # 混淆矩阵：直接显示个数
    confusion = confusion_matrix(label_test, label_predict)
    # 混淆矩阵：转换为概率
    confusion_prob = np.zeros([5, 5])
    for first_index in range(len(confusion)):
        for second_index in range(len(confusion[first_index])):
            sum_row = np.sum(confusion, 1)  # total number of true label
            confusion_prob[first_index, second_index] = \
                float(confusion[first_index][second_index] / sum_row[first_index])

    # plt.imshow(confusion, cmap=plt.cm.Blues)       # 格子背景颜色基于个数
    plt.imshow(confusion_prob, cmap=plt.cm.Blues)    # 格子背景颜色基于概率

    # 混淆矩阵的横纵坐标名称、图例、横纵坐标名称：
    plt.title(title, fontsize=14)
    indices = ['Wake', 'S1', 'S2', 'SWS', 'REM']
    tick_marks = np.arange(len(indices))

    plt.xticks(tick_marks, indices, fontproperties=myfont)
    plt.yticks(tick_marks, indices, fontproperties=myfont)
    plt.colorbar()

    plt.ylim(len(indices) - 0.5, -0.5)
    plt.ylabel('True sleep stage', fontsize=14)
    plt.xlabel('Predicted sleep stage', fontsize=14)
    for first_index in range(len(confusion)):
        for second_index in range(len(confusion[first_index])):
            # 1. 直接绘制数值
            # plt.text(second_index, first_index, confusion[first_index][second_index])
            # 2. 绘制概率
            sum_row = np.sum(confusion, 1)  # total number of true label

            if confusion[first_index][second_index] / sum_row[first_index] < 0.7:
                plt.text(second_index - 0.2, first_index + 0.05,
                         decimal.Decimal("%.2f" % float(confusion[first_index][second_index] / sum_row[first_index])),
                         )
            else:
                plt.text(second_index-0.2, first_index+0.05,
                         decimal.Decimal("%.2f" % float(confusion[first_index][second_index] / sum_row[first_index])),
                         color='w')

    plt.show()

def kappa(Confusion_Matrix):
    n = np.sum(Confusion_Matrix)
    sum_po = 0
    sum_pe = 0
    for i in range(len(Confusion_Matrix[0])):
        sum_po += Confusion_Matrix[i][i]
        row = np.sum(Confusion_Matrix[i, :])
        col = np.sum(Confusion_Matrix[:, i])
        sum_pe += row * col
    po = sum_po / n
    pe = sum_pe / (n * n)
    k = (po - pe) / (1 - pe)
    return k