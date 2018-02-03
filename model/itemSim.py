import math
import sys

import pymysql

from static import dataSet as ds

#计算并载入书籍相似度到BookSimilarity表，计算并载入书籍热门度到BookPopularity表

book_similarity_matrix ={}      #书籍相似度矩阵
book_popularity = {}            #有借阅记录的书籍和对应的借阅人数（popularity）

class ItemSimilarity(object):

    def cal_book_similarity(self):
        for user, books in ds.trainset.items():
            for book in books:
                # count item popularity，这里movie_popular[movie]即给物品movie打分的用户数
                if book not in book_popularity:
                    book_popularity[book] = 0
                book_popularity[book] += 1

        print('count books number and popularity succ', file=sys.stderr)

        # save the total number of books
        book_count = len(book_popularity)
        print('total book number = %d' % book_count, file=sys.stderr)

        # count co-rated users between items
        itemsim_mat = book_similarity_matrix
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
        print('calculating movie similarity matrix...', file=sys.stderr)

        for m1, related_books in itemsim_mat.items():  #m1, m2类似于i,j
            MAX_Wij= 0
            for m2, count in related_books.items():
                itemsim_mat[m1][m2] = count / math.sqrt(
                    book_popularity[m1] * book_popularity[m2])
                if itemsim_mat[m1][m2]> MAX_Wij:
                    MAX_Wij= itemsim_mat[m1][m2]

            for m2, count in related_books.items():
                itemsim_mat[m1][m2] =itemsim_mat[m1][m2] / MAX_Wij   #物品相似度的归一化
                #print(m1+':'+m2+'='+str(self.book_similarity_matrix[m1][m2]))

        print('calculate book similarity matrix(similarity factor) succ',
              file=sys.stderr)

    def load_book_similarity(self):
        sql_insert_bookSim="INSERT INTO BookSimilarity (book1_id, book2_id, algorithm_type, similarity) VALUES ('%s', '%s', '%d', '%f');"
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        for m1, related_books in book_similarity_matrix.items():
            for m2, count in related_books.items():
                data= (m1, m2, 0, book_similarity_matrix[m1][m2])  #0代表itemcf-IUF + 物品归一化 算法
                try:
                    cursor.execute(sql_insert_bookSim % data)
                except:
                    print('Error: unable to insert!')
        db.commit()
        db.close()
        print('load book similarity into BookSimilarity Table succ',
              file=sys.stderr)

    def load_book_popularity(self):
        sql_insert_bookPor="INSERT INTO BookPopularity (book_id, self.book_popularity) VALUES ('%s', '%d');"
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        for book in book_popularity:
            data= (book, book_popularity[book])
            try:
                cursor.execute(sql_insert_bookPor % data)
            except:
                print('Error: unable to insert!')
        db.commit()
        db.close()
        print('load book popularity into BookPopularity Table succ',
              file=sys.stderr)

    def getBookSimilarity(self, book1id, book2id):
        if (len(book_similarity_matrix) != 0):
            return book_similarity_matrix[book1id][book2id]
        '''
        else:
            self.cal_book_similarity()
            return book_similarity_matrix[book1id][book2id]
        '''
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        sql_query_sim = "SELECT similarity FROM BookSimilarity WHERE book1_id= '%s' AND book2_id= '%s';"
        data=(book1id, book2id)
        try:
            cursor.execute(sql_query_sim % data)
        except:
            print("KeyError!")
        for row in cursor.fetchall():
            return row[0]
