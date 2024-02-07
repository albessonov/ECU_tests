import RPi.GPIO as GPIO
import time
import can
import pytest
def test_1():
 bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan')
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 GPIO.output(20,GPIO.LOW)
 time.sleep(1)
 GPIO.output(20,GPIO.HIGH)
 on=time.time()  #start the time counter
 msg = bus.recv(5)#waiting for message
 received=time.time()
 bus.shutdown()
 GPIO.cleanup()
 if(received-on<0.3):
     print("\033[32m Success")
 else:
     print("\033[31m Fail")  

if __name__ == '__main__':
   test_1()



