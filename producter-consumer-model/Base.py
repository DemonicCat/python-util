#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import threading
import Queue
import logging
import time
import traceback
import sys 

def get_logger(self, path=None):
    logger = logging.getLogger("threading_eg")
    logger.setLevel(logging.WARNING)
    path = path or './log/app.log'
    log_dir = os.path.dirname(path)
    lock.acquire()
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    lock.release()
    #fh = logging.FileHandler(path)
    from logging.handlers import TimedRotatingFileHandler
    fh = TimedRotatingFileHandler(path,
                                  when = 'S',
                                  interval = 5,
                                  backupCount=7)
    fmt = '%(asctime)s - %(name)s - %(processName)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    fh.close()
    return logger

class ConsumerThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, queue, logger, statuspath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue
        self.logger = logger
        self.statuspath = statuspath
    
    def run(self):     #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print "Starting " + self.name
        while True:
            try:
                global c_flag
                if not self.queue.empty() and c_flag:
                    data = self.queue.get(block=True, timeout=10)#接收消息 
                    self.method(data)
                    self.queue.task_done()#完成一个任务
                else:
                    #print self.name,' Waiting'
                    time.sleep(1)
            except:
                traceback.print_exc()
                self.queue.task_done()#完成一个任务
                break
  
        with open(self.statuspath, 'ab') as f:
            f.write('Exiting' + self.name + '\n')
        print "Exiting " + self.name

    def method(self, data):
        path = os.path.join(dir_path, data)
        json_file = path
        num = os.listdir(path)
        global file_num
        lock.acquire()
        file_num += len(num)
        print file_num
        lock.release()



class Producter(threading.Thread):
    """生产者线程"""
    def __init__(self, threadID, name, queue, offset, statuspath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue
        self.datas = []
        self.putdatas = []
        self.offset = offset
        self.statuspath = statuspath
        self.iteration = 1
        
    def run(self):
        with open(self.statuspath, 'ab') as f:
            f.write(str(time.ctime()) + '\n')
        while True:
            try:
                global c_flag
                if self.queue.empty():
                    c_flag = False
                    self.read_datas(self.iteration)
                    if not self.datas:
                        break
                    for data in self.putdatas:
                        self.queue.put(data, block=True, timeout=None)
                    print 'Wait for finish'
                    self.iteration += 1
                c_flag = True
                time.sleep(1)
                #self.queue.join()
            except Exception as err:
                print err
                print 'Producter break'
                break
        print 'Producter break'
        os._exit(0) #退出主线程
        #sys.exit() #不能完全kill主线程

    def read_datas(self, iteration):
        try:
            if not self.datas:
                records = os.listdir(dir_path)
                if records:
                    self.datas.extend(records)
                    self.putdatas =  self.datas[(iteration-1)*self.offset : iteration*self.offset]
            else:
                if iteration*self.offset <= len(self.datas):
                    self.putdatas = self.datas[(iteration-1)*self.offset : iteration*self.offset]
                else:
                    self.putdatas = self.datas[(iteration-1)*self.offset:]
        except Exception as err:
            print err
            
if __name__ == '__main__':
    dir_path = '/mnt/234_iscdata/md7/人脸图片抓取/dayre'
    file_num = 0
    maxsize = 100
    threadnum = 50
    logpath = "./log/queue.log"
    logger = get_logger()
    statuspath = "queue_status.log"
    c_flag = False #线程控制开关
    threadlist = []
    lock = threading.RLock()
    q = Queue.Queue(maxsize)    
    p = Producter(0, 'Thread-Producter', q, maxsize, statuspath)
    p.start()
    for i in range(threadnum):
        t = ConsumerThread(i, 'Thread-%d' % i, q, logger, statuspath)
        threadlist.append(t)
    for t in threadlist:
        t.setDaemon(True)  #守护线程
        t.start()
    for t in threadlist:
        t.join()           
