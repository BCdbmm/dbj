# coding=utf-8
# 医学界
# 加载分类模型
# 孙玉龙

# 代码规范: PEP 8

# 编译日期:
# 2019-2-21

# 编译环境:
# Python 3.6.5 64位
# PyCharm 破解版 2018.3, 64位, 英文版
# Windows 10 Version 1803, 64位, 英文版
from scipy.sparse import csr_matrix
import numpy as np
# from sklearn.naive_bayes import MultinomialNB as NB
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
#聚类样本生成器，这里用不到，测试使用
#from sklearn.datasets.samples_generator import make_blobs
#pca不支持sparse输入格式
# from sklearn.decomposition import PCA
#退而求其次，使用svd压缩
from sklearn.decomposition import TruncatedSVD
#导入随机森林，希望进一步提高精准
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
model=joblib.load("lg3.m")
titles=[]
data=[]
fea_row=[]
fea_col=[]
row_index=0
max_col=0
with open("../gen_data/item_code.txt","r",encoding="UTF-8") as h:
    for line in h:
        ss=line.strip().split("\001")
        titles.append(ss[0])
        x=ss[1:]
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
fea_data_set=csr_matrix((data,(row,col)),shape=(row_index,max_col+1))
svd=TruncatedSVD(30)
svd.fit(fea_data_set)
x_new=svd.fit_transform(fea_data_set)
# predict=model.predict(x_new)
# print(predict)
predict=model.predict_proba(x_new)
f=open("end_of_classify.txt","w",encoding="UTF-8")
dicts={}
for i in range(len(predict)):
    title=titles[i]
    score=predict[i,1]
    print("\t".join([title,str(score)]))
    label=1
    if score<0.5:
        label = 0
    dicts[title]=label
for title,label in sorted(dicts.items(),key=lambda x:x[1],reverse=True):
    f.write("\t".join([title,str(label)]))
    f.write("\n")
f.close()