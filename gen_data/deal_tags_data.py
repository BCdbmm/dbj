# coding=utf-8
# 医学界
# 对文章分词，生成训练数据//没用到
# 孙玉龙

# 代码规范: PEP 8

# 编译日期:
# 2018-11-30

# 编译环境:
# Python 3.6.5 64位
# PyCharm 破解版 2018.3, 64位, 英文版
# Windows 10 Version 1803, 64位, 英文版
#导入jieba分词
import jieba
import jieba.posseg
import jieba.analyse
#读入原始标签文档
data=[]
word_dict={}
with open("../data_source/meta_tags.txt","r") as h:
    for line in h:
        ss=line.strip().split("\t")
        if len(ss)!=4:continue
        tag=ss[0]
        print(tag,jieba.analyse.extract_tags(tag))
        lv=ss[1]
        pre_lv=ss[2]
        id=ss[3]
        words=[]
        for e in jieba.analyse.extract_tags(tag,withWeight=True):
            if e[0] not in word_dict:
                word_dict[e[0]]=len(word_dict)+1
            s=":".join([str(word_dict[e[0]]),str(e[1])])
            words.append(s)



