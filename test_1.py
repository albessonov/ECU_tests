import RPi.GPIO as GPIO
import time
import can

def test_1():
 bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan')
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
 if(received-on<0.3):
     print("\033[32m Success")
 else:
     print("\033[31m Fail")

if __name__ == '__main__':
   test_1()




