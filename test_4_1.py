import RPi.GPIO as GPIO
import ctypes as ct
import threading
import os
from signal import SIGKILL
import subprocess
import time
TTF=30000 
so_file = "/home/pi/Desktop/tests/c_inserts/subtest.so"
cfunc = ct.CDLL(so_file)
tt = ct.c_long.in_dll(cfunc, 'tt')
def acc():
    cfunc.uart(1)
'''def periodic_send(msg, bus):
    task = bus.send_periodic(msg, 0.100)
    assert isinstance(task, can.CyclicSendTaskABC)
    return task'''
def test_4():
 pid=os.getpid()
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 accel=threading.Thread(target=acc)
 accel.start()
 time.sleep(10)
 print("TTF,µS:",tt.value/1000)
 if(tt.value<TTF+3000 and tt.value>TTF-3000):
     print("\033[32m Success")
 else:
     print("\033[31m Fail")    
 GPIO.cleanup()
 #cfunc.terminate()
 os.kill(pid, SIGKILL)
 
if __name__ == '__main__':
    test_4()



