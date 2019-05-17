# coding=utf-8
# 医学界
# 对文章分词，生成训练数据,步骤2
# 孙玉龙

# 代码规范: PEP 8

# 编译日期:
# 2019-2-21

# 编译环境:
# Python 3.6.5 64位
# PyCharm 破解版 2018.3, 64位, 英文版
# Windows 10 Version 1803, 64位, 英文版
import jieba
import jieba.analyse
data=[]
items_data=[]
feat_set=set()
with open("../data_source/good_data/dbj.txt","r",encoding="UTF-8") as h:
    for line in h:
        ss=line.strip().split("\001")
        title=ss[0]
        content=ss[2]
        label="1"
        tag_score=jieba.analyse.textrank(title+content,topK=100,withWeight=True)
        li=[]
        for e in tag_score:
            li.append(e)
            feat_set.add(e[0])
        data.append((label,li))
        items_data.append((title,li))
i=0
with open("../data_source/good_data/notdbj.txt","r",encoding="UTF-8") as h:
    i+=1
    for line in h:
        ss=line.strip().split("\001")
        title=ss[0]
        content=ss[2]
        label="0"
        tag_score=jieba.analyse.textrank(title+content,topK=100,withWeight=True)
        li = []
        for e in tag_score:
            li.append(e)
            feat_set.add(e[0])
        items_data.append((title, li))
        data.append((label,li))
        # data.append((label, li))
        # if i%3==0:
        #     data.append((label, li))

feat_id_dict={}
for n,e in enumerate(feat_set):
    feat_id_dict[e]=n
with open("feat_id.txt","w",encoding="UTF-8") as f:
    for k,v in feat_id_dict.items():
        f.write("\001".join([k,str(v)]))
        f.write("\n")
with open("item_code.txt","w",encoding="UTF-8") as h:
    for dd in items_data:
        title = dd[0]
        ll = []
        ll.append(title)
        for e in dd[1]:
            key, score = e
            ll.append(":".join([str(feat_id_dict[key]), str(score)]))
        s = "\001".join(ll)
        h.write(s)
        h.write("\n")
f=open("sample.txt","w",encoding="UTF-8")
for dd in data:
    label=dd[0]
    ll=[]
    ll.append(label)
    for e in dd[1]:
        key,score=e
        ll.append(":".join([str(feat_id_dict[key]),str(score)]))
    s=" ".join(ll)
    f.write(s)
    f.write("\n")
f.close()