# pip install psutil
import os
from time import sleep
import psutil
import _thread
import time
import subprocess
import timeit

if __name__ == "__main__":
    demo_environment = {**os.environ,}

    try:
        AppName = str("C:/xiping/CMakeTestPrj/cmake_test_install/build/install/testprj.exe")
        Cfg = str("C:/xiping/chenwei803/person_analysis/build/install/config.json")
        if AppName[len(AppName)-3 : len(AppName) : 1]!="exe":
            AppName = AppName + str(".exe")

        if os.path.exists(AppName):
            start_time = timeit.default_timer()
            print("Start: ", AppName)
            subprocess.check_output(AppName,
                timeout=6,
                stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8',
                env=demo_environment)
            execution_time = timeit.default_timer() - start_time
            print("execution_time: ", execution_time)
        else:
            print("No exist: ", AppName)
    except subprocess.TimeoutExpired as e_timeout:
        print(e_timeout.output)
        print('Exit code: timeout 600')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print('Exit code:', e.returncode)