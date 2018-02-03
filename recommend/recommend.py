import sys
from operator import itemgetter

from model import itemSim as its
from model import userSim as us
from static import dataSet as ds


class Recommend(object):

    def __init__(self, user, k, recom_nums, algo_type):
        self.rank = {}
        self.borrowed_books = ds.trainset[user]
        self.K = k
        self.N = recom_nums
        self.user= user
        self.algorithm_type= algo_type
    '''
    def recommend_by_itemcf(self): #从数据库BookSimilarity导入相似度数据
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
            for related_book, similarity_factor in sorted(self.book_sim_mat[book].items(),
                                                           key=itemgetter(1), reverse=True)[:self.K]:
                if related_book in self.borrowed_books: #推荐没借过的书
                    continue
                self.rank.setdefault(related_book, 0)
                self.rank[related_book] += similarity_factor  #因为是一元数据，所以rating不用
        # return the topN movies
        return sorted(self.rank.items(), key=itemgetter(1), reverse=True)[:self.N]
    '''
    def start_recommend(self):
        if (self.algorithm_type == 0):
            return self.recommend_by_itemcf()
        if (self.algorithm_type == 1):
            return self.recommend_by_usercf()

    def recommend_by_itemcf(self):
        if (len(its.book_similarity_matrix) == 0):   #避免重复计算相似度矩阵
            its.ItemSimilarity().cal_book_similarity()

        for book, rating in self.borrowed_books.items():
            # related_book：与该书籍相似的书籍
            # similarity_factor：两个书籍的相似度
            for related_book, similarity_factor in sorted(its.book_similarity_matrix[book].items(),
                                                          key=itemgetter(1), reverse=True)[:self.K]:
                if related_book in self.borrowed_books:  # 推荐没借过的书
                    continue
                self.rank.setdefault(related_book, 0)
                self.rank[related_book] += similarity_factor  # 因为是一元数据，所以rating不用
        # return the topN movies
        self.rank = sorted(self.rank.items(), key=itemgetter(1), reverse=True)[:self.N]

        #for book, _ in self.rank:
        #    print('recommend book id: %s' % book, file=sys.stderr)  # 输出推荐结果的书籍id
        return self.rank

    def recommend_by_usercf(self):
        if (len(us.user_similarity_matrix) == 0):   #避免重复计算相似度矩阵
            us.UserSimilarity().cal_user_similarity()

        for similar_user, similarity_factor in sorted(us.user_similarity_matrix[self.user].items(),
                                                      key=itemgetter(1), reverse=True)[0:self.K]:
            for book in ds.trainset[similar_user]:
                if book in self.borrowed_books:
                    continue
                self.rank.setdefault(book, 0)
                self.rank[book] += similarity_factor
        # return the N best movies
        self.rank = sorted(self.rank.items(), key=itemgetter(1), reverse=True)[0:self.N]
        #for book, _ in self.rank:
        #    print('recommend book id: %s' % book, file=sys.stderr)  # 输出推荐结果的书籍id
        return self.rank