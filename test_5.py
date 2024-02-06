import RPi.GPIO as GPIO
import can
from ctypes import *
import threading
import os
from signal import SIGKILL
import subprocess
import time
so_file = "/home/pi/Desktop/tests/c_inserts/subtest.so"
cfunc = CDLL(so_file)
def acc():
    cfunc.uart(3)
'''def periodic_send(msg, bus):
    task = bus.send_periodic(msg, 0.100)
    assert isinstance(task, can.CyclicSendTaskABC)
    return task'''
def test_5():
 pid=os.getpid()
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 #speed = can.Message(arbitration_id=0x5D7, data=[0, 0, 0, 0, 0, 0, 0x1e, 0xFF], is_extended_id=False) #vehicle speed 79.35 km/h
 #periodic_send(speed,bus)
 accel=threading.Thread(target=acc)
 accel.start()
 k=subprocess.Popen(['candump','can0,023:7FF', '-td', '-n5'])
 time.sleep(15)
 #bus.shutdown()
 GPIO.cleanup()
 os.kill(pid, SIGKILL)
if __name__ == '__main__':
    test_5()
