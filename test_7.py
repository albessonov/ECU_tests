import time
import can
import pytest
def test7():
 bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan')
 enter=can.Message(arbitration_id=0x752,is_extended_id=False)
 request=can.Message(arbitration_id=0x752,data=[0x3,0x22,0xC9,0x53],is_extended_id=False)
 bus.send(enter)#to enter diag session
 bus.send(request)
 response = bus.recv(timeout=10)#waiting for message
 print(hex(response.data[0]),hex(response.data[1]),hex(response.data[2]),hex(response.data[3]),hex(response.data[4]))
 if(response.data[0]==0x4 and response.data[1]==0x62 and response.data[2]==0xC9 and response.data[3]==0x53 and response.data[4]==0):
     print("\033[32m Success")
 else:
     print("\033[31m Failed") 
 bus.shutdown()

 
if __name__ == "__main__":
    test7()
