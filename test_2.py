import RPi.GPIO as GPIO
import time
import can
import pytest
import subprocess
'''def periodic_send(msg, bus):
    task = bus.send_periodic(msg, 0.100)
    assert isinstance(task, can.CyclicSendTaskABC)
    return task'''
def test_2():
 timelist = [] 
 #filters = [{"can_id": 0x653, "can_mask": 0x7FF,"extended": False},]
 #bus=can.Bus(channel='vcan0',receive_own_messages=False,interface='socketcan',can_filters=filters)
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 #msg = can.Message(arbitration_id=0x653, data=[0, 0, 0, 0, 0, 0, 0x1e, 0xFF], is_extended_id=False) #vehicle speed 79.35 km/h
 #periodic_send(msg,bus)
 k=subprocess.Popen(['candump','can0,653:7FF', '-td', '-n50','T50000'],stdout=subprocess.PIPE)
 for i in range(0,50):
  line = k.stdout.readline()
  a=line[4:11]
  res=float(a)
  timelist.append(res)
  print(res)
 ctr=0 
 for i in range(1,50):
   print(timelist[i])
   if(timelist[i]>=0.11 or timelist[i]<=0.09):
     ctr+=1;
 if(ctr==0):
  print("Success")
 else:
  print("Fail")  
GPIO.cleanup()
 

if __name__ == '__main__':
    test_2()
