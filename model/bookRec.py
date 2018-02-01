import pymysql
import math
import os
import sys
from operator import itemgetter
from model import dataSet as ds
from model import itemSim as its

class BookRec(object):

    def __init__(self, user, k, recom_nums):
        self.rank = {}
        self.borrowed_books = ds.trainset[user]
        self.K = k
        self.N = recom_nums
        self.book_sim_mat = {}

    def recommend_by_dataset(self): #从数据库BookSimilarity导入相似度数据
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        for book, rating in self.borrowed_books.items(): #针对用户的每个借过（评分过）的书，进行找前K个相似书籍查找
            self.book_sim_mat.setdefault(book, {})
            sql_query_simbook = "SELECT book2_id, similarity FROM BookSimilarity WHERE book1_id= '%s';"
            try:
                cursor.execute(sql_query_simbook % book)
            except:
                print("Error!")
            for row in cursor.fetchall():
                self.book_sim_mat[book][row[0]] = row[1]
            # related_book：与该书籍相似的书籍
            # similarity_factor：两个书籍的相似度
            for related_book, similarity_factor in sorted(self.book_sim_mat[book].items(),
                                                           key=itemgetter(1), reverse=True)[:self.K]:
                if related_book in self.borrowed_books: #推荐没借过的书
                    continue
                self.rank.setdefault(related_book, 0)
                self.rank[related_book] += similarity_factor  #因为是一元数据，所以rating不用
        # return the topN movies
        return sorted(self.rank.items(), key=itemgetter(1), reverse=True)[:self.N]


    def recommend_by_generateSim_Mat(self): #每次都再计算一遍相似度矩阵后导入相似度数据
        its.ItemSimilarity().cal_book_similarity()
        for book, rating in self.borrowed_books.items():
            for related_book, similarity_factor in sorted(its.book_similarity_matrix[book].items(),
                                                          key=itemgetter(1), reverse=True)[:self.K]:
                if related_book in self.borrowed_books:  # 推荐没借过的书
                    continue
                self.rank.setdefault(related_book, 0)
                self.rank[related_book] += similarity_factor  # 因为是一元数据，所以rating不用
        # return the topN movies
        return sorted(self.rank.items(), key=itemgetter(1), reverse=True)[:self.N]