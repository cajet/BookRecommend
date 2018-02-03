import math
import sys
import pymysql

from static import dataSet as ds

#计算并载入用户相似度到UserSimilarity表

user_similarity_matrix ={}      #书籍相似度矩阵
book_popularity = {}            #有借阅记录的书籍和对应的借阅人数（popularity）
book2users = dict()             #book-users inverse table

class UserSimilarity(object):
    
    def cal_user_similarity(self):

        print ('building book-users inverse table...', file=sys.stderr)
        for user, books in ds.trainset.items():
            for book in books:
                # inverse table for item-users
                if book not in book2users:
                    book2users[book] = set()
                book2users[book].add(user)
                # count item popularity at the same time
                if book not in book_popularity:
                    book_popularity[book] = 0
                book_popularity[book] += 1
        print ('build book-users inverse table succ', file=sys.stderr)

        book_count = len(book2users)
        print ('total book number = %d' % book_count, file=sys.stderr)

        # count co-rated items between users
        usersim_mat = user_similarity_matrix
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


    def load_user_similarity(self):
        self.cal_user_similarity()
        sql_insert_userSim="INSERT INTO UserSimilarity (card1_id, card2_id, algorithm_type, similarity) VALUES ('%s', '%s', '%d', '%f');"
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        for m1, related_books in user_similarity_matrix.items():
            for m2, count in related_books.items():
                data= (m1, m2, 1, user_similarity_matrix[m1][m2])  #1代表usercf算法
                try:
                    cursor.execute(sql_insert_userSim % data)
                except:
                    print('Error: unable to insert!')
        db.commit()
        db.close()
        print('load user similarity into UserSimilarity Table succ',
              file=sys.stderr)

    def getUserSimilarity(self, card1id, card2id):
        if (len(user_similarity_matrix) != 0):
            return user_similarity_matrix[card1id][card2id]
        '''
        else:
            self.cal_user_similarity()
            return user_similarity_matrix[card1id][card2id]
        '''
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        sql_query_sim = "SELECT similarity FROM UserSimilarity WHERE card1_id= '%s' AND card2_id= '%s';"
        data=(card1id, card2id)
        try:
            cursor.execute(sql_query_sim % data)
        except:
            print("KeyError!")
        for row in cursor.fetchall():
            return row[0]