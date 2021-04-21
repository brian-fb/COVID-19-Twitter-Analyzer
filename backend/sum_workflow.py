import os,time
from multiprocessing import Process
from Summarization.sum_updator import sum_updator
from Data.spark_engine import spark_engine

if __name__=='__main__':

    # Creat a thread for spark engine
    p1 = Process(target=spark_engine, name="worker1", args=())
    # Creat a thread for sum updator
    p2 = Process(target=sum_updator,name="worker2",args=())
    p1.start()
    p2.start()