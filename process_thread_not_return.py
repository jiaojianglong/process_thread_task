#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 21:56
# @Author  : jiaojianglong

import os
import time
import threading
import concurrent.futures

ProcessThreadExecutor = {} #非进程安全的
process_executor = concurrent.futures.ProcessPoolExecutor()  # 创建进程池，参数可指定进程数量，如果不指定按系统cup核数，max_works = 4


def future_process(func,fun,*args,**kwargs):
    process_executor.submit(func,fun,*args,**kwargs)#将任务提交到进程池，参数必须pickleable（不可使用装饰器）
    #process_executor.map(func,iterable)#函数一样时可以批量提交

def future_thread(func,*args,**kwargs):
    print("分配进程：",os.getpid())
    if os.getpid() in ProcessThreadExecutor.keys():
        thread_executor = ProcessThreadExecutor[os.getpid()]
    else:
        print("使用新创建线程")
        thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)#在进程池中的进程里创建线程池。
        ProcessThreadExecutor[os.getpid()] = thread_executor
    thread_executor.submit(func,*args,**kwargs)#将任务提交到线程池，返回一个future对象
    time.sleep(0.01)#进程主线程任务执行太快，会导致所有任务都分配到一个进程中，所以加一点耗时操作。


def process_thread_run_task(fun,*args,**kwargs):
    future_process(future_thread, fun,*args,**kwargs)

def fun(i):
    time.sleep(3)
    print("我是第%s条"%i,"执行进程",os.getpid(),"执行线程",threading.current_thread().getName())
    return "我的执行进程"+ str(os.getpid()) + "执行线程" + threading.current_thread().getName()

if __name__ == "__main__":
    for i in range(400):
        process_thread_run_task(fun,i)