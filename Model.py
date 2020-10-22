import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from Myfunctions import PerformanceMetrics, My_ConfusionMatrix
from sklearn import svm
from sklearn import metrics
import scipy.io as scio
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer
 

if __name__ == '__main__':

    direcction = 'newDataSet/'

    CHAN = [[3,5,11],
        [3,4],
        [8,9,11,12,13,14,15],
        [11,14],
        [3,8,9,12,15,18]]

    for i in range(1,6):
        chan = CHAN[i-1]
        inds_del = []
        for j in range(0,len(chan)):
            inds_del += list(range( (chan[j]-1)*6 ,chan[j]*6))
        
        dataFile = direcction + 'train/S' + str(i) + '_train_features.mat'
        data = scio.loadmat(dataFile)
        anntationFile = direcction + 'train/S' + str(i) + '_train_labels.mat'
        anntation = scio.loadmat(anntationFile)
        testFile = direcction + 'test/S' + str(i) + '_test_features.mat'
        testdata = scio.loadmat(testFile)

        feature_array = data['train_features']
        annotation_array = anntation['train_labels']
        testdata_array = testdata['test_features']

        feature_array = np.delete(feature_array, inds_del, axis=1)
        testdata_array = np.delete(testdata_array, inds_del, axis=1)

        annotation_array = annotation_array.ravel()
        # 划分训练集和测试集：
        feature_tmp, feature_test, annotation_tmp, annotation_test = train_test_split(
            feature_array, annotation_array, test_size=0.3, stratify=annotation_array, random_state = 1)

        # 划分训练集和验证集：
        feature_train, feature_val, annotation_train, annotation_val = train_test_split(
            feature_tmp, annotation_tmp, test_size=0.3, stratify=annotation_tmp, random_state=1)


        # 线性判别器调参
        svc = LinearDiscriminantAnalysis()

        parameters = [
            {
                'solver': ['svd'],
                'priors': [[0.2,0.8],[0.1,0.9],[0.3,0.7]],
            },
            {
                'solver': ['lsqr', 'eigen'],
                'shrinkage': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            }
        ]
        clf = GridSearchCV(svc, parameters, cv=10, n_jobs=8,scoring=make_scorer(metrics.f1_score))
        clf.fit(feature_array, annotation_array)
        print(clf.best_params_)
        best_model = clf.best_estimator_
        best_model.fit(feature_train, annotation_train)
        p300_predict = best_model.predict(feature_val)
        accCurr = metrics.accuracy_score(p300_predict, annotation_val)
        precCurr = metrics.precision_score(p300_predict, annotation_val)
        F1Curr = metrics.f1_score(p300_predict, annotation_val)
        
        print([F1Curr, accCurr, precCurr])

        # final_p300_predict = clf.predict(testdata_array)
        # pred = final_p300_predict
        # for n in range(0,len(pred)):
        #     if pred[n] == 1:
        #         print(str(n//12+1) + '  ' + str((n+1)%12))
        # print()
