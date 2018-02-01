import pymysql
import math
import os
import sys
from model import dataSet as ds
from model import bookRec as br

if __name__ == '__main__':
    ds.dataset()   #执行里面的初始化给全局变量trainset,testset赋值
    rank = {}
    temp= br.BookRec('14331000', 20, 10)
    rank= temp.recommend_by_generateSim_Mat()
    for book, _ in rank:
        print('recommend book id: %s' % book, file= sys.stderr)  #输出推荐结果的书籍id
