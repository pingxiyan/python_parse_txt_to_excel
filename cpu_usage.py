# pip install psutil
import os
from time import sleep
import psutil
import _thread
import time

g_exit_flag = False
list_cpu_util = []

def thrd_fun_get_cpu_util(thrd_name):
    global list_cpu_util
    global g_exit_flag

    for i in range(0XFFFFFFFF):
        list_cpu_util.append(psutil.cpu_percent(interval=1))
        if g_exit_flag:
            break
        sleep(1)

def get_cpu_util():
    try:
        _thread.start_new_thread(thrd_fun_get_cpu_util, ( "Thread-1", ))
    except:
        print("Error: unable to start thread")

if __name__ == "__main__":
    get_cpu_util()
    print("main sleep 5.")
    time.sleep(10)
    g_exit_flag = True

    print("list_cpu_util: ", list_cpu_util)