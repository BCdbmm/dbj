# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 11:48
# @Author  : sunyulong
# @Email   : sunyulong@yxj.org.cn
# @File    : test.py
# @Software: PyCharm
# @Standard: PEP 8

from io import StringIO
#使用的是pdfminer.six库，pdfminer不能用
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
# import sys, getopt
import re
#使用的是python-docx库，docx库不能用
import docx

# converts pdf, returns its text content as a string
def convert(pathlist, outpath1, outpath2, pages=None):
    """
    从docx和pdf提取text
    :param pathlist: 输入文件的路径a.pdf放在这里
    :param outpath1: 输出文件路径(我自己项目需要文章分类，两个路径)
    :param outpath2: 输出文件路径2
    :param pages:设置提取页面数
    :return:None
    """
    c = ["生坐挫璧型筮查Q生旦箜坐鲞筮翅堡i』盟型趔：』些型Q：些丝：塑：",
         "生堡』b型苤查生旦筮鲞筮翅垦堕』堕堕：Q笪Q：：i：盟：",
         "生生挂经处型盘盎生且基垫鲞筮期处．旦』盟￡婴强。』Y．垫堡J型：堡，：",
         "虫堡翌丝型蓥圭生旦箜堑鲞笙塑垦i』堕翌：型盟：∑：堑：盟：",
         "主堡塑经型苤查堡生旦笠12鲞筮塑g也』盟塑：e堂：：垒：堕：66l·",
         "生堡益丝处型盘查至旦笙鲞箜塑堡堕』丛业竺业婆：』Q：y：：：",
         "虫堡翌丝型蓥圭生旦箜堑鲞笙塑垦i』堕翌：型盟：∑：堑：盟：",
         "生坐挫璧型筮查Q生旦箜坐鲞筮翅堡i』盟型趔：』些型Q：些丝：塑：",
         "空堡垄经处型苤圭生旦筮鲞箜塑堡也』盟塑垡：』z：y：：盟：",
         ""
         ]
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    h1 = open(outpath1, "w", encoding="UTF-8")
    h2 = open(outpath2, "w", encoding="UTF-8")
    for path in pathlist:
        if path.find("guide") >= 0:
            content_type = "指南"
        elif path.find("news") >= 0:
            content_type = "新闻"
        elif path.find("activate") >= 0:
            content_type = "活动"
        for file in os.listdir(path):
            if file.endswith("pdf"):
                output = StringIO()
                manager = PDFResourceManager()
                converter = TextConverter(manager, output, laparams=LAParams())
                interpreter = PDFPageInterpreter(manager, converter)
                fname = path + file
                print(fname)
                infile = open(fname, 'rb')
                for page in PDFPage.get_pages(infile, pagenums):
                    interpreter.process_page(page)
                infile.close()
                converter.close()
                text = output.getvalue()
                output.close()
                s = text.replace("\n", " ")
                r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
                res = re.sub(r, "", s).replace(" ", "")
                for e in c:
                    res = res.replace(e, "")
            else:
                fname = path + file
                doc = docx.Document(fname)
                res = ""
                for para in doc.paragraphs:
                    strs = para.text.replace("\n", "").strip("\n")
                    if len(strs) == 0: continue
                    res += (strs + ".")
            if path.find("notdbj") >= 0:
                arts = "\001".join([file, "其他", res])
                h2.write(arts)
                h2.write("\n")
            else:
                arts = "\001".join([file, content_type, res])
                h1.write(arts)
                h1.write("\n")
    h1.close()
    h2.close()



if __name__ == "__main__":
    pathlist=["../data_source/guide/pdf/",
              "../data_source/guide/docx/",
              "../data_source/news/",
              "../data_source/activate/",
              "../data_source/notdbj/"
              ]
    outpath1="../data_source/good_data/dbj.txt"
    outpath2="../data_source/good_data/notdbj.txt"
    convert(pathlist,outpath1,outpath2)