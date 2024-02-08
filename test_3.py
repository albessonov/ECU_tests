import RPi.GPIO as GPIO
import can
import time
import subprocess
import threading
import struct
from ctypes import *
so_file = "/home/albessonov/tests/c_inserts/subtest.so"
cfunc = CDLL(so_file)
def acc():
    cfunc.uart(1)
def test3():
 timelist = [] 
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 accel=threading.Thread(target=acc)
 accel.start()
 k=subprocess.Popen(['candump','can0,023:7FF', '-td', '-n50','-T50000'],stdout=subprocess.PIPE)
 for i in range(0,50):
  line = k.stdout.readline()
  a=line[4:11]
  res=float(a)
  timelist.append(res)
  print(res)
 ctr=0 
 for i in range(1,50):
   print(timelist[i])
   if(timelist[i]>=0.0044 or timelist[i]<=0.0036):
    ctr+=1
 k.kill()    
 GPIO.cleanup()
 if(ctr==0):
     print("\033[32m Success")
 else:
     print("\033[31m Fail")    

if __name__ == '__main__':
   test3()