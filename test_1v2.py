
import RPi.GPIO as GPIO
import time
import can
def test_1():
 bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan')
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #turn on the power
 print("waiting for IO2 state change")
 GPIO.wait_for_edge(17, GPIO.RISING)
 on=time.time()  #start the time counter 
 print('State change detected.')
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
