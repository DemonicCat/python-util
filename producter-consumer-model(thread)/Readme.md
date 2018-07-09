待改进：

*线程挂掉后，没有重启线程机制，考虑修改

*多个线程取出同队列里同一个数据，造成混乱，queue.get时，加锁解决

*使用threading.event()事件控制线控

*上下文管理

threading 模块的对象 Lock、 RLock、 Condition、 Semaphore 和 BoundedSemaphore 都包含
上下文管理器，也就是说,它们都可以使用 with 语句

```
def loop(nsec):
    myname = currentThread().name 
    with lock: 
        remaining.add(myname)
```
