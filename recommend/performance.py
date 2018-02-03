import sys
import math
import pymysql
from operator import itemgetter
from model import itemSim as its
from model import userSim as us
from static import dataSet as ds
from recommend import recommend as rc

class Performance(object):

    def __init__(self, recom_nums, k, Algorithm_Type):
        self.precision = 0
        self.recall = 0
        self.coverage = 0
        self.popularity = 0
        self.algorithm_type= Algorithm_Type
        self.N = recom_nums
        self.K= k

        self.hit = 0
        self.rec_count = 0                        #给所有人推荐的书籍数目之和
        self.test_count = 0                       #测试集中所有用户借阅的书籍数目之和
        # varables for coverage
        self.all_rec_books = set()                #所有推荐的书籍集合
        # varables for popularity
        self.popular_sum = 0
        self.rec_books = {}                        #给每个用户推荐的书籍
        self.book_popularity={}

    def evaluate(self):
        for i, user in enumerate(ds.trainset):  #验证推荐命中的原理：看trainset中给用户推荐的书籍是否在testset对应的用户的借阅书籍中
            if i % 500 == 0:
                print ('recommended for %d users' % i, file=sys.stderr)
            test_books = ds.testset.get(user, {})

            self.rec_books = rc.Recommend(user, self.K, self.N, self.algorithm_type).start_recommend()
            if (self.algorithm_type == 0):
                self.book_popularity= its.book_popularity
            if (self.algorithm_type == 1):
                self.book_popularity= us.book_popularity

            for book, _ in self.rec_books:
                if book in test_books:
                    self.hit += 1
                self.all_rec_books.add(book)
                self.popular_sum += math.log(1 + self.book_popularity[book])
            self.rec_count += self.N
            self.test_count += len(test_books)

        self.precision = self.hit / (1.0 * self.rec_count)
        self.recall = self.hit / (1.0 * self.test_count)
        self.coverage = len(self.all_rec_books) / (1.0 * len(self.book_popularity))
        self.popularity = self.popular_sum / (1.0 * self.rec_count)

        print ('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' %
               (self.precision, self.recall, self.coverage, self.popularity), file=sys.stderr)

    def loadperformance(self):
        self.evaluate()
        sql_insert_performance = "INSERT INTO Performance (algorithm_type, k, precision_, recall, coverage, popularity) " \
                                 "VALUES ('%d', '%d', '%f', '%f', '%f', '%f');"
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        data= (self.algorithm_type, self.K, self.precision, self.recall, self.coverage, self.popularity)
        cursor.execute(sql_insert_performance % data)
        db.commit()
        db.close()