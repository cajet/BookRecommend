import pymysql

trainset={}
testset={}

class dataset(object):

    def __init__(self):
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()

        sql_query_train = "SELECT card_id, book_id, mark FROM BorrowTable WHERE testdata= 0;"
        cursor.execute(sql_query_train)
        for row in cursor.fetchall():
            trainset.setdefault(row[0], {})
            trainset[row[0]][row[1]] = row[2]

        sql_query_test = "SELECT card_id, book_id, mark FROM BorrowTable WHERE testdata= 1;"
        cursor.execute(sql_query_test)
        for row in cursor.fetchall():
            testset.setdefault(row[0], {})
            testset[row[0]][row[1]] = row[2]

        db.commit()
        db.close()
        #print("给全局变量trainset, testset赋值完毕!")

