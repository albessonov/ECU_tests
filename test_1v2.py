'''IO2 физически притянут к питанию, с IO2 тест запустить невозможно '''


import RPi.GPIO as GPIO
import time
import can
def test_1():
 bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan')
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #turn on the power
 GPIO.wait_for_edge(2, GPIO.RISING)
 on=time.time()  #start the time counter   
 msg = bus.recv(3)#waiting for message
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
