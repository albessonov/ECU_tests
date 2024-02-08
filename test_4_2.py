import RPi.GPIO as GPIO
import ctypes as ct
import threading
import os
from signal import SIGKILL
import subprocess
import time
TTF=12000
so_file = "/home/pi/Desktop/tests/c_inserts/subtest.so"
cfunc = ct.CDLL(so_file)
tt = ct.c_long.in_dll(cfunc, 'tt')
def acc():
    cfunc.uart(2)
'''def periodic_send(msg, bus):
    task = bus.send_periodic(msg, 0.100)
    assert isinstance(task, can.CyclicSendTaskABC)
    return task'''
def test_4():
 pid=os.getpid()
 #filters = [{"can_id": 0x023, "can_mask": 0x7FF,"extended": False},]
 #bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan',can_filters=filters)
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 #speed = can.Message(arbitration_id=0x5D7, data=[0, 0, 0, 0, 0, 0, 0x1e, 0xFF], is_extended_id=False) #vehicle speed 79.35 km/h
 #periodic_send(speed,bus)
 accel=threading.Thread(target=acc)
 accel.start()
 time.sleep(5)#изменить
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
