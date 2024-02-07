import RPi.GPIO as GPIO
import ctypes as ct
import threading
import os
import can
from signal import SIGKILL
import subprocess
import time
so_file = "/home/pi/Desktop/tests/c_inserts/subtest.so"
cfunc = ct.CDLL(so_file)
tt = ct.c_long.in_dll(cfunc, 'tt')
def acc():
    cfunc.uart(4)
def test_5():
 pid=os.getpid()
 bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan')
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 accel=threading.Thread(target=acc)
 accel.start()
 msg=bus.recv(5)
 print(msg)
 if(msg==None and (tt.value>1000000 or tt.value==0)): #tt=0 в случае, если момент 0с не был пройден и на IO21(IO26) не пришел сигнал; tt>1000000 в случае, если произошло что-то одно
     print("\033[32m Success")
 else:
     print("\033[31m Fail")
 GPIO.cleanup()
 os.kill(pid, SIGKILL)
if __name__ == '__main__':
    test_5()
