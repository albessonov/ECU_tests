import RPi.GPIO as GPIO
import time
import can
import pytest
def test7():
 bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan')
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 enter=can.Message(arbitration_id=0x752,is_extended_id=False)
 request=can.Message(arbitration_id=0x752,data=[0x3,0x22,0xC9,0x53],is_extended_id=False)
 bus.send(enter)#to enter diag session
 bus.send(request)
 response = bus.recv(timeout=300)#waiting for message
 print(hex(response.data))
 if(response.data[0]==0x4 and response.data[1]==0x62 and response.data[2]==0xC9 and response.data[3]==0x53 and response.data[4]==0):
     print("\033[32m Success")
 else:
     print("\033[31m Failed") 
 GPIO.output(20, GPIO.LOW)#power off
 bus.shutdown()
 GPIO.cleanup()
 
if __name__ == "__main__":
    test7()
