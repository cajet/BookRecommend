import sys
import os
import pymysql
import time
from model import dataSet as ds

if __name__ == '__main__':
    start = time.clock()
    db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
    cursor = db.cursor()
    sql_query_similarity="SELECT similarity FROM BookSimilarity WHERE book1_id='%s' AND book2_id='%s';"
    try:
        data=('3793','1')
        cursor.execute(sql_query_similarity % data)
    except:
        print("Error!")
    for row in cursor.fetchall():
        print(row[0])
    end = time.clock()
    print(end - start)