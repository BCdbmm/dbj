# coding=utf-8
# 医学界
# 根据分类结果，对只包含dbj文章做分词
# 孙玉龙

# 代码规范: PEP 8

# 编译日期:
# 2019-02-22

# 编译环境:
# Python 3.6.5 64位
# PyCharm 破解版 2018.3, 64位, 英文版
# Windows 10 Version 1803, 64位, 英文版
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import jieba
import numpy as np
import jieba.analyse
dbj_=[]
with open("end_of_classify.txt","r",encoding="UTF-8") as f:
    for line in f:
        ss=line.strip().split("\t")
        if len(ss)!=2:continue
        dbj_.append(ss[0])
tf_dict={}
with open("article.txt","r",encoding="UTF-8") as f:
    for line in f:
        ss=line.strip().split("\001")
        if len(ss)!=3:continue
        if ss[0] not in dbj_:continue
        title=ss[0]
        content=ss[1]
        title_keyword=jieba.analyse.textrank(title)
        content_keyword=jieba.analyse.textrank(content)
        # title_keyword = jieba.analyse.textrank(title, withWeight=True)
        # content_keyword = jieba.analyse.textrank(content, withWeight=True)
        for w in title_keyword:
            if w not in tf_dict:
                tf_dict[w]=0
            tf_dict[w]+=1
        for w in content_keyword:
            if w not in tf_dict:
                tf_dict[w]=0
            tf_dict[w]+=1
new_tf=dict(sorted(tf_dict.items(),key=lambda x:x[1],reverse=True))
X=np.array([k for k,v in new_tf.items()][:30])
Y=np.array([v for k,v in new_tf.items()][:30])
fig,ax=plt.subplots()
b=ax.barh(range(len(X)),Y,color='#6699CC')
ax.set_yticks(range(len(X)))
ax.set_yticklabels(X)
plt.show()
with open("token_frequency.txt","w",encoding="UTF-8") as h:
    for k,v in new_tf.items():
        if v<0.01:continue
        h.write("\t".join([k,str(v)]))
        h.write("\n")
        print("\t".join([k,str(v)]))
