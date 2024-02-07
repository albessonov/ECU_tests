import RPi.GPIO as GPIO
import time
import can
import pytest
import subprocess

def test_2():
 timelist = [] 
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(20, GPIO.OUT,initial=GPIO.HIGH) #turn on the power
 k=subprocess.Popen(['candump','can0,653:7FF', '-td', '-n50'],stdout=subprocess.PIPE)
 for i in range(0,50):
  line = k.stdout.readline()
  a=line[4:11]
  res=float(a)
  timelist.append(res)
  print(res)
 ctr=0 
 for i in range(1,50):
     if (timelist[i]<=0.11 and timelist[i]>=0.09):
          ctr+=0
     else:
          ctr+=1
 if(ctr==0):
     print("\033[32m Success")
 else:
     print("\033[31m Fail")      
 GPIO.cleanup()
 

if __name__ == '__main__':
    test_2()
