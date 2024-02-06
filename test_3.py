import RPi.GPIO as GPIO
import can
import time
import subprocess
import threading
import struct
from ctypes import *
so_file = "/home/pi/Desktop/tests/c_inserts/subtest.so"
cfunc = CDLL(so_file)
def acc():
    cfunc.uart(1)
'''def periodic_send(msg, bus):
    task = bus.send_periodic(msg, 0.100)
    assert isinstance(task, can.CyclicSendTaskABC)
    return task'''
def test3():
 timelist = [] 
 filters = [{"can_id": 0x023, "can_mask": 0x7FF,"extended": False}]
 bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan',can_filters=filters)
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 accel=threading.Thread(target=acc)
 accel.start()
 k=subprocess.Popen(['candump','can0,023:7FF', '-td', '-n50'],stdout=subprocess.PIPE)
 for i in range(0,50):
  line = k.stdout.readline()
  a=line[4:11]
  res=float(a)
  timelist.append(res)
  #print(res)
 for i in range(1,50):
   print(timelist[i])
     #assert(timelist[i]<=0.0044)
     #assert(timelist[i]>=0.0036)
 GPIO.cleanup()
 bus.shutdown()
 p.kill()

if __name__ == '__main__':
   test3()
