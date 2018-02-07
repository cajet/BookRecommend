#-*- coding: utf-8 -*-
'''
Created on 2018-01-20

@author: Cajet
'''
import sys
import random
import math
import os
from static import dataSet as ds
from operator import itemgetter
import pymysql

book_sim_mat = {}
user_sim_mat = {}
user_sim_mat2 = {}
book_popular = {}

class Item_UserBasedCF(object):

    def __init__(self, k, n):
        self.new_trainset = {}
        self.n_sim_book = k
        self.n_rec_book = n
        self.n_sim_user = k
        self.h= 15
        self.book_count = 0

    def calc_book_sim(self):

        for user, books in ds.trainset.items():
            for book in books:
                # count item popularity，这里book_popular[book]即给物品book打分的用户数
                if book not in book_popular:
                    book_popular[book] = 0
                book_popular[book] += 1

        # save the total number of books
        self.book_count = len(book_popular)

        # count co-rated users between items
        itemsim_mat = book_sim_mat
        print('building co-rated users matrix...', file=sys.stderr)

        for user, books in ds.trainset.items():
            for m1 in books:
                for m2 in books:
                    if m1 == m2:
                        continue
                    itemsim_mat.setdefault(m1, {})
                    itemsim_mat[m1].setdefault(m2, 0)
                    itemsim_mat[m1][m2] += 1 / math.log(1+len(books)*1.0)  #ItemCF-IUF 减小用户活跃度对物品相似度的影响

        print('build co-rated users matrix succ', file=sys.stderr)

        # calculate similarity matrix
        print('calculating book similarity matrix...', file=sys.stderr)

        for m1, related_books in itemsim_mat.items():  #m1, m2类似于i,j
            MAX_Wij= 0
            for m2, count in related_books.items():
                itemsim_mat[m1][m2] = count / math.sqrt(
                    book_popular[m1] * book_popular[m2])
                if itemsim_mat[m1][m2]> MAX_Wij:
                    MAX_Wij= itemsim_mat[m1][m2]
            for m2, count in related_books.items():
                itemsim_mat[m1][m2] =itemsim_mat[m1][m2] / MAX_Wij   #物品相似度的归一化

        print('calculate book similarity matrix(similarity factor) succ',
              file=sys.stderr)


    def calc_user_sim(self):
        book2users = dict()

        for user, books in ds.trainset.items():
            for book in books:
                # inverse table for item-users
                if book not in book2users:
                    book2users[book] = set()
                book2users[book].add(user)
        print ('build book-users inverse table succ', file=sys.stderr)

        # count co-rated items between users
        usersim_mat = user_sim_mat
        print ('building user co-rated books matrix...', file=sys.stderr)

        for book, users in book2users.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    usersim_mat.setdefault(u, {})
                    usersim_mat[u].setdefault(v, 0)
                    usersim_mat[u][v] += 1/ math.log(1+len(users)*1.0)
        print ('build user co-rated books matrix succ', file=sys.stderr)

        # calculate similarity matrix
        print ('calculating user similarity matrix...', file=sys.stderr)

        for u, related_users in usersim_mat.items():
            for v, count in related_users.items():
                usersim_mat[u][v] = count / math.sqrt(
                    len(ds.trainset[u]) * len(ds.trainset[v]))

        print ('calculate user similarity matrix(similarity factor) succ',
               file=sys.stderr)

    def calc_user_sim2(self):
        book2users = dict()

        for user, books in self.new_trainset.items():
            for book in books:
                # inverse table for item-users
                if book not in book2users:
                    book2users[book] = set()
                book2users[book].add(user)
        print ('build book-users inverse table succ', file=sys.stderr)

        # count co-rated items between users
        usersim_mat = user_sim_mat2
        print ('building user co-rated books matrix...', file=sys.stderr)

        for book, users in book2users.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    usersim_mat.setdefault(u, {})
                    usersim_mat[u].setdefault(v, 0)
                    usersim_mat[u][v] += 1/ math.log(1+len(users)*1.0)
        print ('build user co-rated books matrix succ', file=sys.stderr)

        # calculate similarity matrix
        print ('calculating user similarity matrix...', file=sys.stderr)

        for u, related_users in usersim_mat.items():
            for v, count in related_users.items():
                usersim_mat[u][v] = count / math.sqrt(
                    len(self.new_trainset[u]) * len(self.new_trainset[v]))

        print ('calculate user similarity matrix(similarity factor) succ',
               file=sys.stderr)

    def cal_IH(self, user):
        rank = {}
        borrowed_books = ds.trainset[user]
        for book, rating in borrowed_books.items():
            for related_book, similarity_factor in book_sim_mat[book].items():
                if related_book in borrowed_books: #推荐没看过的电影
                    continue
                rank.setdefault(related_book, 0)
                rank[related_book] += similarity_factor * rating
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:self.h]  # h= 5

    def cal_UK(self, user):
        K = self.n_sim_user
        return sorted(user_sim_mat[user].items(), key=itemgetter(1), reverse=True)[0:K]

    def generate_new_trainset(self):
        for i, user in enumerate(ds.trainset):
            IH = self.cal_IH(user)
            UK = self.cal_UK(user)
            for book, _ in IH:  # 在训练集中添加该用户对这5本书的评分
                sum = 0
                count = 0
                for sim_user, _ in UK:
                    try:
                        sum = sum + ds.trainset[sim_user][book]
                        count= count+1
                    except:  # 若邻居用户没有对book进行评分
                        pass
                if (count!= 0):
                    ave = sum / count   #取平均值，注意这里是除以实际评分的人数，而不是K
                    self.new_trainset[user][book] = ave
        print('generate new trainset succ', file=sys.stderr)

    def recommend(self, user):
        K = self.n_sim_book
        N = self.n_rec_book
        rank = dict()
        borrowed_books = ds.trainset[user]

        for similar_user, similarity_factor in sorted(user_sim_mat2[user].items(),
                                                      key=itemgetter(1), reverse=True)[0:K]:
            for book in ds.trainset[similar_user]:
                if book in borrowed_books:
                    continue
                rank.setdefault(book, 0)
                rank[book] += similarity_factor * ds.trainset[similar_user][book]
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    def evaluate(self):
        N = self.n_rec_book
        hit = 0
        rec_count = 0
        test_count = 0
        # varables for coverage
        all_rec_books = set()
        # varables for popularity
        popular_sum = 0

        for i, user in enumerate(ds.trainset):
            test_books = ds.testset.get(user, {})
            rec_books = self.recommend(user)
            for book, _ in rec_books:
                if book in test_books:
                    hit += 1
                all_rec_books.add(book)
                popular_sum += math.log(1 + book_popular[book])
            rec_count += N
            test_count += len(test_books)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_books) / (1.0 * len(book_popular))
        popularity = popular_sum / (1.0 * rec_count)

        print ('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' %
               (precision, recall, coverage, popularity), file=sys.stderr)

        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        sql_insert_performance = "INSERT INTO Performance (algorithm_type, k, precision_, recall, coverage, popularity) " \
                                 "VALUES ('%d', '%d', '%f', '%f', '%f', '%f');"
        data = (2, self.n_sim_book, precision, recall, coverage, popularity)
        cursor.execute(sql_insert_performance % data)
        db.commit()
        db.close()

if __name__ == '__main__':
    ratingfile = os.path.join('ml-1m', 'new_ratings.dat')
    ds.dataset()
    db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
    cursor = db.cursor()
    sql_query_train = "SELECT card_id, book_id, mark FROM BorrowTable WHERE testdata= 0;"

    Item_UserBasedCF(20, 10).calc_book_sim()
    Item_UserBasedCF(20, 10).calc_user_sim()

    item_usercf = Item_UserBasedCF(20, 10)
    cursor.execute(sql_query_train)
    for row in cursor.fetchall():
        item_usercf.new_trainset.setdefault(row[0], {})
        item_usercf.new_trainset[row[0]][row[1]] = row[2]
    item_usercf.generate_new_trainset()
    item_usercf.calc_user_sim2()
    item_usercf.evaluate()



