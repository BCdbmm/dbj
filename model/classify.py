# coding=utf-8
# 医学界
# 训练分类模型
# 孙玉龙

# 代码规范: PEP 8

# 编译日期:
# 2019-02-22

# 编译环境:
# Python 3.6.5 64位
# PyCharm 破解版 2018.3, 64位, 英文版
# Windows 10 Version 1803, 64位, 英文版
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

#pca不支持sparse输入格式
# from sklearn.decomposition import PCA
#退而求其次，使用svd压缩
from sklearn.decomposition import TruncatedSVD

#导入随机森林，希望进一步提高精准
from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
mlp=MLPClassifier(solver='lbfgs', activation='relu',alpha=1e-5,hidden_layer_sizes=(30, 10), random_state=1)
SVM=SVC(kernel="sigmoid",probability=True)
lg=LogisticRegression()
nb=BayesianRidge()
forest=RandomForestClassifier(n_estimators=20)
label=[]
data=[]
fea_row=[]
fea_col=[]
row_index=0
max_col=0
with open("../gen_data/sample.txt","r",encoding="UTF-8") as h:
    for line in h:
        ss=line.strip().split(" ")
        y=ss[0]
        x=ss[1:]
        label.append(int(y))
        for fs in x:
            arr=fs.split(":")
            if len(arr)!=2:continue
            feat=arr[0]
            score=arr[1]
            data.append(float(score))
            fea_row.append(row_index)
            fea_col.append(int(feat))
            if int(feat)>max_col:
                max_col=int(feat)
        row_index+=1
row=np.array(fea_row)
col=np.array(fea_col)
data=np.array(data)
print(type(data))
print(type(row))
print(type(col))
fea_data_set=csr_matrix((data,(row,col)),shape=(row_index,max_col+1))
svd=TruncatedSVD(30)
svd.fit(fea_data_set)
x_new=svd.fit_transform(fea_data_set)
# pca=PCA(n_components=30)
# pca.fit(fea_data_set)
# x_new=pca.transform(fea_data_set)
xtrain,xtest,ytrain,ytest=train_test_split(x_new,label,test_size=0.2)
lg.fit(xtrain,ytrain)
nb.fit(xtrain,ytrain)
forest.fit(xtrain,ytrain)
SVM.fit(xtrain,ytrain)
mlp.fit(xtrain,ytrain)
print("------------")
print(lg.score(xtest,ytest))
print(np.mean(lg.predict(xtest)-ytest)**2)
print(lg.score(xtrain,ytrain))
print(np.mean(lg.predict(xtrain)-ytrain)**2)
print("------------")
print(nb.score(xtest,ytest))
print(np.mean(nb.predict(xtest)-ytest)**2)
print(forest.score(xtest,ytest))
print(np.mean((forest.predict(xtest)-ytest)**2))
print(SVM.score(xtest,ytest))
print(np.mean((SVM.predict(xtest)-ytest)**2))
print(mlp.score(xtest,ytest))
print(np.mean((mlp.predict(xtest)-ytest)**2))
#训练了4个模型，分别是测试集为80%，70%，50%，30%的效果
joblib.dump(lg,"lg3.m")
joblib.dump(nb,"nb3.m")
joblib.dump(forest,"rf3.m")
joblib.dump(SVM,"svm3.m")
joblib.dump(mlp,"mlp3.m")