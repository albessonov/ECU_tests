import time
import can
import pytest
import random

def keygen(seed, rnd):
    key=seed
    Mask03=0xD2944523
    if(rnd<(255-35)):
        rnd+=35
    else: rnd=255
    for i in range(1,rnd+1):
        if((key&0x80000000)!=0):
            key=(key<<1)^Mask03;
        else: key<<=1
    return key
'''
def keygen(seed):
    key=seed
    Mask = 0x36583001 
    for i in range(0,35):
        if((seed&0x80000000)!=0):
            seed=(seed<<1)^Mask;
        else: seed<<=1
    key=seed    
    return key'''
    

def test8():
 rnd=random.randint(0,255)
 #rnd=0x33
 bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan')
 enter=can.Message(arbitration_id=0x752,is_extended_id=False)
 request=can.Message(arbitration_id=0x752,data=[0x3,0x27,0x1,rnd],is_extended_id=False)
 bus.send(enter)#to enter diag session
 bus.send(request)
 response = bus.recv(timeout=300)#waiting for message
 print(hex(response.data[0]),hex(response.data[1]),hex(response.data[2]),hex(response.data[3]),hex(response.data[4]))
 #assert(response.data[1]==0x67)#checking for positive response to request seed
 seed=(response.data[2]<<24)|(response.data[3]<<16)|(response.data[4]<<8)|(response.data[5])
 print("seed:",hex(seed))
 key=keygen(seed,rnd)
 key1=key&0xffffffff
 print("key:",hex(key1))
 firstbyte=key1>>24
 secondbyte=(key1>>16&0xff)
 thirdbyte=(key1>>8&0xff)
 fourthbyte=key1&0xff
 #print(hex(firstbyte),hex(secondbyte),hex(thirdbyte),hex(fourthbyte))
 sendkey=can.Message(arbitration_id=0x752,data=[0x6,0x27,0x02,firstbyte,secondbyte,thirdbyte,fourthbyte],is_extended_id=False)
 bus.send(sendkey)
 sendkey_response=bus.recv(30)
 print(hex(sendkey_response.data[0]),hex(sendkey_response.data[1]))
 if(sendkey_response.data[0]==0x67 and sendkey_response.data[1]==0x2):#positive response
     print("\033[32m Success")
 else:
     print("\033[31m Fail")
 bus.shutdown()
 
if __name__ == "__main__":
    test8()
