from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
import time
import logging
import subprocess
import threading
import struct
import RPi.GPIO as GPIO
import can
from ctypes import *
import _ctypes
import os
from signal import SIGQUIT
import random


class Tester(QObject):
    progress = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.__process_handle = None
        self.__is_enabled = False
        self.is_emulating = False
        self.stop_requested = False
        self.pattern = 1
        self.so_filet3 = "/home/pi/Desktop/tests/c_inserts/subtest.so"
        if not self.is_emulating:
            self.cfunct3 = CDLL(self.so_filet3)
            
    def acc(self, pattern):
        self.cfunc.uart(pattern)
    def isLoaded(self, lib):#
        libp = os.path.abspath(lib)#
        ret = os.system("lsof -p %d | grep %s > /dev/null" % (os.getpid(), libp))#
        return (ret == 0)#
    def dlclose(self,handle):#
        libdl = CDLL("/lib/aarch64-linux-gnu/libdl.so.2")#
        libdl.dlclose(handle) #   
    def keygen(self, seed, rnd):
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
    
    @pyqtSlot(int)
    def do_test(self, n):
        self.stop_requested = False
        logging.info(f"Started test {n} execution")
        if n == 1:
            self.test_1()
        elif n == 2:
            self.test_2()
        elif n == 3:
            self.test_3()
        elif n == 4:
            self.test_4()
        elif n == 5:
            self.test_5()
        elif n == 6:
            self.test_6()
        logging.info(f"Test {n} completed")

    def test_1(self):
        if self.is_emulating:
            for i in range(5):
                time.sleep(0.5)
                results = dict()
                results["can"] = f"test can msg {i}"
                self.progress.emit(results)

            results = dict()
            results["val"] = f"295 мс"
            results["res"] = f"Пройден успешно"
            self.progress.emit(results)
        else:
            results = dict()
            bus=can.Bus(channel='can0',receive_own_messages=True,interface='socketcan')
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #turn on the power
            logging.info("waiting for IO17 state change")
            GPIO.wait_for_edge(17, GPIO.RISING)
            on=time.time()  #start the time counter 
            logging.info('State change detected.')
            msg = bus.recv(5)#waiting for message
            received=time.time()
            logging.info(msg)
            bus.shutdown()
            GPIO.cleanup()
            tim = received-on
            print(received-on)
            logging.info(1000*tim)
            results["val"] = f"{round(1000*tim, 3)} мс"
            results["can"] = f"ID:      653    S Rx                DL:  4    00 c0 00 00                 Channel: can0"
            if(received-on<0.3):
                logging.info("TEST 1 Success")
                results["res"] = f"Success"
            else:
                logging.info("TEST 2 Fail")
                results["res"] = f"Fail"
            self.progress.emit(results)

    def test_2(self):
        if self.is_emulating:
            for i in range(5):
                time.sleep(0.5)
                results = dict()
                results["can"] = f"test can msg {i}"
                self.progress.emit(results)

            results = dict()
            results["val"] = f"10 мс"
            results["res"] = f"Пройден успешно"
            self.progress.emit(results)
        else:
            results = dict()
            timelist = [] 
            k=subprocess.Popen(['candump','can0,653:7FF', '-td', '-n50','-T50000'],stdout=subprocess.PIPE)
            for i in range(0,50):
                line = k.stdout.readline()
                results["can"] = line.decode()
                self.progress.emit(results)
                a=line[4:11]
                res=float(a)
                timelist.append(res)
                logging.info(res)
            ctr=0
            period = 0
            for i in range(1,50):
                if (timelist[i]<=0.11 and timelist[i]>=0.09):
                    ctr+=0
                else:
                    ctr+=1
                period += timelist[i]
            period /= 49
            results["val"] = f"{round(period*1000, 3)} мс"
            if(ctr==0):
                results["res"] = f"Success"
                logging.info("TEST 2 Success")
            else:
                results["res"] = f"Fail"
                logging.info("TEST 2 Fail")  
            self.progress.emit(results)

    def test_3(self):
        if self.is_emulating:
            for i in range(5):
                time.sleep(0.5)
                results = dict()
                results["can"] = f"test can msg {i}"
                self.progress.emit(results)

            results = dict()
            results["val"] = f"10 мс"
            results["res"] = f"Пройден успешно"
            self.progress.emit(results)
        else:
            results = dict()
            timelist = [] 
            test_pattern = 1
            accel=threading.Thread(target=self.cfunct3.uart,args=(test_pattern,))
            accel.start()
            k=subprocess.Popen(['candump','can0,023:7FF', '-td', '-n50','-T50000'],stdout=subprocess.PIPE)
            for i in range(0,50):
                line = k.stdout.readline()
                results["can"] = line.decode()
                self.progress.emit(results)
                a=line[4:11]
                res=float(a)
                timelist.append(res)
                logging.info(res)
            ctr=0 
            period_4ms = 0
            for i in range(1,50):
                logging.info(timelist[i])
                if(timelist[i]>=0.0044 or timelist[i]<=0.0036):
                    ctr+=1
                period_4ms += timelist[i]
            period_4ms = period_4ms/49*1000
            results["val"] = f"{round(period_4ms, 3)} мс"
            k.kill()    
            if(ctr==0):
                results["res"] = f"Success"
                logging.info("TEST 3 Success")
            else:
                results["res"] = f"Fail"
                logging.info("TEST 3 Fail")  
            self.progress.emit(results)

    def test_4(self):
        test_pattern = self.pattern
        if(test_pattern==1):
            so_file = "/home/pi/Desktop/tests/c_inserts/subtest1.so"#
        elif(test_pattern==2):
            so_file = "/home/pi/Desktop/tests/c_inserts/subtest2.so"#
        elif(test_pattern==3):
            so_file = "/home/pi/Desktop/tests/c_inserts/subtest3.so"#
        elif(test_pattern==4):
            so_file = "/home/pi/Desktop/tests/c_inserts/subtest4.so"#
        else:
            print("wrong pattern")            
        cfunc = CDLL(so_file)#
        if self.is_emulating:
            time.sleep(1)
            results = dict()
            results["res"] = f"Пройден успешно, TTF=X мс"
            self.progress.emit(results)
        else:
            results = dict()
            tt = c_long.in_dll(cfunc, 'tt')#
            timeX = c_float.in_dll(cfunc, 'timeX')#
            flag=c_bool.in_dll(cfunc, 'flag')#
            if(test_pattern==1):
                TTF=30000
            elif(test_pattern==2):    
                TTF=12000
            else:
                TTF=0
            pid=os.getpid()
            accel=threading.Thread(target=cfunc.uart,args=(test_pattern,))
            accel.start()
            if(test_pattern==1 or test_pattern==2):
                while True:
                    if(tt.value>0):
                        logging.info(f"TTF,uS:{int(tt.value/1000)}")
                        break
                if((tt.value/1000)<TTF+3000 and (tt.value/1000)>TTF-3000):
                    logging.info("TEST 4 Success")
                    results["res"] = f"Success, TTF={round(tt.value/1000000, 3)} мс"
                    #results["val"] = f"{round(tt.value/1000, 3)} мс"
                else:
                    logging.info("TEST 4 Fail")
                    results["res"] = f"Fail, TTF={round(tt.value/1000000, 3)} мс"
                    #results["val"] = f"{round(tt.value/1000, 3)} мс"
            if(test_pattern==3 or test_pattern==4):
                time.sleep(10)
                if(tt.value==0 and timeX.value>-100.0): 
                    logging.info("TEST 4 Success")
                    results["res"] = f"Success"
                else:
                    logging.info("TEST 4 Fail")
                    results["res"] = f"Fail"
            self.progress.emit(results)
            #os.kill(pid, SIGQUIT)
            flag=0
            time.sleep(20)
            _ctypes.dlclose(cfunc._handle)
            print("ready")
            

    def test_5(self):
        if self.is_emulating:
            for i in range(5):
                time.sleep(0.5)
                results = dict()
                results["can"] = f"test can msg rx {i}"
                results["can_tx"] = f"test can msg tx {i}"
                self.progress.emit(results)

            results = dict()
            results["res"] = f"Пройден успешно"
            self.progress.emit(results)
        else:
            results = dict()
            filters = [{"can_id": 0x752, "can_mask": 0x7FF, "extended": False}]
            bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan',can_filters=filters)
            #enter=can.Message(arbitration_id=0x752,is_extended_id=False)
            request=can.Message(arbitration_id=0x752,data=[0x3,0x22,0xC9,0x53],is_extended_id=False)
            #results["can_tx"] = f"{enter}"
            #self.progress.emit(results) 
            results["can_tx"] = f"{request}"
            #bus.send(enter)#to enter diag session
            bus.send(request)
            response = bus.recv(timeout=10)#waiting for message
            results["can"] = f"{response}"
            print(hex(response.data[0]),hex(response.data[1]),hex(response.data[2]),hex(response.data[3]),hex(response.data[4]))
            if(response.data[0]==0x4 and response.data[1]==0x62 and response.data[2]==0xC9 and response.data[3]==0x53 and response.data[4]==0):
                results["res"] = f"Success"
                logging.info("TEST 5 Success") 
            else:
                results["res"] = f"Fail"
                logging.info("TEST 5 Fail") 
            self.progress.emit(results)

    def test_6(self):
        if self.is_emulating:
            for i in range(5):
                time.sleep(0.5)
                results = dict()
                results["can"] = f"test can msg {i}"
                results["can_tx"] = f"test can msg tx {i}"
                self.progress.emit(results)

            results = dict()
            results["res"] = f"Пройден успешно"
            self.progress.emit(results)
        else:
            results = dict()
            rnd=random.randint(0,255)
            filters = [{"can_id": 0x752, "can_mask": 0x7FF, "extended": False}]
            bus=can.Bus(channel='can0',receive_own_messages=False,interface='socketcan',can_filters=filters)
            DiagSession=can.Message(arbitration_id=0x752,data=[0x02,0x10,0x3],is_extended_id=False)
            #request to enter ExtendedDiagnosticSession
            request_seed=can.Message(arbitration_id=0x752,data=[0x3,0x27,0x1,rnd],is_extended_id=False)
            bus.send(DiagSession)#to enter extended diagnostic session
            sended_diag_session = dict()
            DiagSession_response=bus.recv(100)
            logging.info(DiagSession_response)
            bus.send(request_seed)
            requestseed_response = bus.recv(timeout=100)#waiting for message
            logging.info(requestseed_response)
            seed=((requestseed_response.data[3])<<24)|(requestseed_response.data[4]<<16)|(requestseed_response.data[5]<<8)|(requestseed_response.data[6])
            #print("seed:",hex(seed))
            key=self.keygen(seed,rnd)
            key1=key&0xffffffff
            #print("key:",hex(key1))
            #print("key:",hex(key))
            #print("rnd:",hex(rnd))
            firstbyte=key1>>24
            secondbyte=(key1>>16&0xff)
            thirdbyte=(key1>>8&0xff)
            fourthbyte=key1&0xff
            #print(hex(firstbyte),hex(secondbyte),hex(thirdbyte),hex(fourthbyte))
            sendkey=can.Message(arbitration_id=0x752,data=[0x6,0x27,0x02,firstbyte,secondbyte,thirdbyte,fourthbyte],is_extended_id=False)
            bus.send(sendkey)
            sendkey_response=bus.recv(300)
            logging.info(sendkey_response)
            #print(hex(sendkey_response.data[0]),hex(sendkey_response.data[1]))
            if(sendkey_response!=None and sendkey_response.data[1]==0x67 and sendkey_response.data[2]==0x2):#positive response
               logging.info("TEST 6 Success")
               results["res"] = f"Success"
            else:
               logging.info("TEST 6 Fail")
               results["res"] = f"Fail"
            results["can_tx"] = f"{DiagSession}\n{request_seed}\n{sendkey}"
            results["can"] = f"{DiagSession_response}\n{requestseed_response}\n{sendkey_response}" 
            self.progress.emit(results)
            bus.shutdown()
