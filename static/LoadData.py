# -*- coding: UTF-8 -*-

'''
载入图书和借阅记录数据到BookTable和BorrowTable
'''

import pymysql
import sys
import os
import random

random.seed(0)

db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
cursor = db.cursor()

def loadfile(filename):
    fp = open(filename, 'r')
    for i, line in enumerate(fp):
        yield line.strip('\r\n')
    fp.close()

def loadBook(filename):
    for line in loadfile(filename):
        id, name= line.split('::')
        sql = "INSERT INTO BookTable (book_name) VALUES ('%s');"
        try:
            data= (name)
            cursor.execute(sql % data)
        except:
            print('Error: unable to insert!')
        db.commit()
    print('load %s succ' % filename, file=sys.stderr)

def loadBorrowTable(filename, pivot=0.7):
    sql_insert_borrow = "INSERT INTO BorrowTable (card_id, book_id, book_name, mark, testdata) VALUES ('%s', '%s', '%s', '%d', '%d');"
    for line in loadfile(filename):
        user, bookid, rating= line.split('::')
        sql_query_bookname = "SELECT book_name FROM BookTable WHERE id = '%d';"
        if random.random() < pivot:  #训练数据
            try:
                cursor.execute(sql_query_bookname % int(bookid))  #根据书id找书名
                for row in cursor.fetchall():
                    print(row[0])
                    data = (user, bookid, row[0], int(rating), 0)
                    cursor.execute(sql_insert_borrow % data)
            except:
                print('Error: unable to insert!')

        else:                        #测试数据
            try:
                cursor.execute(sql_query_bookname % int(bookid))  #根据书id找书名
                for row in cursor.fetchall():
                    print(row[0])
                    data = (user, bookid, row[0], int(rating), 1)
                    cursor.execute(sql_insert_borrow % data)
            except:
                print('Error: unable to insert!')
        db.commit()
    print('load %s succ' % filename, file=sys.stderr)


if __name__ == '__main__':
    loadBook(os.path.join('dataset', 'books.dat'))
    loadBorrowTable(os.path.join('dataset', 'ratings.dat'))
    db.close()