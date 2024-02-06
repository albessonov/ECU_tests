import RPi.GPIO as GPIO
import time
import can
import pytest
def test_1():
 bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan')
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 time.sleep(1)
 GPIO.output(20, GPIO.LOW)#power off   
 on=time.time()  #start the time counter
 msg = bus.recv(1)#waiting for message
 received=time.time()
 bus.shutdown()
 GPIO.cleanup()
 print(received-on)
if __name__ == '__main__':
   test_2()




