import time

from recommend import recommend as rec
from static import dataSet as ds
from recommend import performance as pf

if __name__ == '__main__':

    ds.dataset()  # 执行里面的初始化给全局变量trainset,testset赋值
    '''
    start= time.clock()
    rec.Recommend('14331000', 20, 10).recommend_by_itemcf()
    end= time.clock()
    print(end-start)
    
    start3 = time.clock()
    pf.Performance(10, 20, 0).evaluate()
    end3 = time.clock()
    print(end3 - start3)
    '''




