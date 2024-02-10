#include <stdio.h>
#include <string.h>
#include "SPI_Messages.h"
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <math.h>
#include <time.h>
#include "pigpio.h"
#include "stdbool.h"
void aFunction(int gpio, int level, uint32_t tick);
struct timespec mt1, mt2;
long int tt;
float timeX=-100,timeY=-100;
bool flag=0;
uint8_t uart (uint8_t test_pattern)//1,2-срабатывание; 3,4-несрабатывание
{
char pathX[]="/home/albessonov/tests/c_inserts/Front XGF 100% 50kmh_?.txt";
char pathY[]="/home/albessonov/tests/c_inserts/Front XGF 100% 50kmh_?.txt";

if(test_pattern==1)
{
strcpy(pathX,path1885X);
strcpy(pathY,path1885Y);
}
else if(test_pattern==2)
{
strcpy(pathX,pathFRONTX);
strcpy(pathY,pathFRONTY);
}
else if(test_pattern==3)
{
strcpy(pathX,path1882X);
strcpy(pathY,path1882Y);
}
else if(test_pattern==4)
{
strcpy(pathX,path1883X);
strcpy(pathY,path1883Y);
}
else
{
printf("Wrong pattern");
exit(1);
}
//part which is responsible for capture edge
gpioInitialise();
gpioSetMode(19,PI_OUTPUT);
gpioSetMode(21,PI_INPUT);
gpioSetPullUpDown(21,PI_PUD_DOWN);
gpioSetISRFunc(21,FALLING_EDGE,-1,aFunction);
///////////
double Num;
unsigned uart1=serialOpen("/dev/ttyAMA0",1500000);

struct Register_Access_Command Register_Read={REGISTER_READ_COMMAND,REGISTER_READ_ADDRESS,REGISTER_READ_DATA,0b00000000};
struct Register_Access_Command Register_Write={REGISTER_WRITE_COMMAND,REGISTER_READ_ADDRESS,REGISTER_READ_DATA,0b00000000};
struct Register_Response Register_Read_Response={(((REGISTER_READ_RESPONSE)<<4)|(ST<<2)|UD),REGISTER_DATA_0,REGISTER_DATA_0,CRC_0};
struct Register_Response Register_Write_Response={(((REGISTER_WRITE_RESPONSE)<<4)|(ST<<2)|UD),REGISTER_DATA_0,REGISTER_DATA_0,CRC_0};

struct Sensor_Data_Request Request0x0={SOURCEID0x00,0,0,0};
struct Sensor_Data_Request Request0x2={SOURCEID0x02,0,0,0};
	//variables to calc CRC
uint32_t Register_Read_32=((Register_Read.Command__Fixed_Bits)<<24)|((Register_Read.Register_Address)<<16)|((Register_Read.Register_Data)<<8);
uint32_t Register_Write_32=((Register_Read.Command__Fixed_Bits)<<24)|((Register_Read.Register_Address)<<16)|((Register_Read.Register_Data)<<8);
uint32_t Register_Read_Response_32=((Register_Read_Response.Command_BS_UD)<<24)|((Register_Read_Response.Register_Data_H)<<16)|((Register_Read_Response.Register_Data_L)<<8);
uint32_t Register_Write_Response_32=((Register_Write_Response.Command_BS_UD)<<24)|((Register_Write_Response.Register_Data_H)<<16)|((Register_Write_Response.Register_Data_L)<<8);

uint32_t Request0x0_32=0x10000000;
uint32_t Request0x2_32=0x50000000;

Request0x0.CRC=CRC8(Request0x0_32);
Request0x2.CRC=CRC8(Request0x2_32);

Register_Read.CRC=CRC8(Register_Read_32);
Register_Write.CRC=CRC8(Register_Write_32);
Register_Read_Response.CRC=CRC8(Register_Read_Response_32);
Register_Write_Response.CRC=CRC8(Register_Write_Response_32);

uint8_t Register_Read_cmd[]={Register_Read.Command__Fixed_Bits,Register_Read.Register_Address,Register_Read.Register_Data,Register_Read.CRC};
uint8_t Register_Write_cmd[]={Register_Write.Command__Fixed_Bits,Register_Write.Register_Address,Register_Write.Register_Data,Register_Write.CRC};
uint8_t Register_Read_Response_cmd[]={Register_Read_Response.Command_BS_UD,Register_Read_Response.Register_Data_H,Register_Read_Response.Register_Data_L,Register_Read_Response.CRC};
uint8_t Register_Write_Response_cmd[]={Register_Write_Response.Command_BS_UD,Register_Write_Response.Register_Data_H,Register_Write_Response.Register_Data_L,Register_Write_Response.CRC};

uint8_t Request0x0cmd[]={Request0x0.Command__Fixed_Bits_0,Request0x0.Fixed_Bits_1,Request0x0.Fixed_Bits_2,Request0x0.CRC};
uint8_t Request0x2cmd[]={Request0x2.Command__Fixed_Bits_0,Request0x0.Fixed_Bits_1,Request0x0.Fixed_Bits_2,Request0x2.CRC};
fp0x0 = fopen(pathX, "r");
if(fp0x0==NULL){printf("Error x");}

fp0x2 = fopen(pathY, "r");
	  if(fp0x2==NULL)
	  printf("Error Y");
while(1)
{
if(flag==1)
{
gpioTerminate();
break;
}
if(timeX==0){
clock_gettime (CLOCK_REALTIME, &mt1);
gpioWrite(19,1);

//printf("%ld\n",mt1.tv_nsec);
}
if(ctr0<0&&ctr2<0) break;
    memset(RXbuf, 0, UART_INPUT_MAX_SIZE);// clean the buf for next reception
    if(serialDataAvail (uart1)!=-1)
    read(uart1,RXbuf,4);
if(memcmp(RXbuf,Register_Read_cmd,sizeof(Register_Read_cmd))==0)
     {
      write(uart1, Register_Read_Response_cmd, sizeof(Register_Read_Response_cmd));
      //close(uart1);
      //exit(0);
     }
else if(memcmp(RXbuf,Register_Write_cmd,sizeof(Register_Write_cmd))==0)
     {
      write(uart1, Register_Write_Response_cmd, sizeof(Register_Write_Response_cmd));
      //close(uart1);
      //exit(0);
	 }
else if(memcmp(RXbuf,Request0x0cmd,sizeof(Request0x0cmd))==0)
     {
         printf("X:%f\n",timeX);
         timeX+=0.5;
		 uint8_t valH0,valL0,valL,valH;
	     fseek(fp0x0,ctr0,0);
	     readstat = getline(&line, &len, fp0x0);
	     ach0=strchr (line,' ');
	     mov0=(ach0-line+1);
		 Num = atof (line);
	     int16_t val=round(20.47*Num);
	     if(val>=0)
	     {
          valL0 = (uint8_t) ((val<<4) & 0x00ff);
          valH0 = (uint8_t) (((val<<4) & 0xff00) >> 8);
          valL=valL0;
          valH=valH0;
	     }
	     else
	     {
          valL0 = (uint8_t) (((-val)<<4) & 0x00ff);
          valH0 = (uint8_t) (((((-val)<<4) & 0xff00) >> 8));
          valL=~valL0+1;
          valH=~valH0;
	     }
         char resp[4];
         resp[0]=(RCOMMAND0x00|(valH>>6));
         resp[1]=((valH<<2)|(valL>>6));
         resp[2]=(valL<<2);
         resp[3]=CRC8((((uint32_t)resp[0])<<24)|(((uint32_t)resp[1])<<16)|(((uint32_t)resp[2])<<8));
	     write(uart1, resp, sizeof(resp));
         ctr0+=mov0;
	 }
else if(memcmp(RXbuf,Request0x2cmd,sizeof(Request0x2cmd))==0)
     {
      printf("Y:%f\n",timeY);
      timeY+=0.5;
	  uint8_t valH0,valL0,valH,valL;
	  fseek(fp0x2,ctr2,0);
	  readstat = getline(&line, &len, fp0x2);
	  ach2=strchr (line,' ');
	  mov2=ach2-line+1;
      Num = atof (line);
	  int16_t val=round(20.47*Num);
      if(val>=0)
	     {
          valL0 = (uint8_t) ((val<<4) & 0x00ff);
          valH0 = (uint8_t) (((val<<4) & 0xff00) >> 8);
          valL=valL0;
          valH=valH0;
	     }
	     else
	     {
          valL0 = (uint8_t) (((-val)<<4) & 0x00ff);
          valH0 = (uint8_t) (((((-val)<<4) & 0xff00) >> 8));
          valL=~valL0+1;
          valH=~valH0;
	     }
      char resp[4];
      resp[0]=(RCOMMAND0x02|(valH>>6));
      resp[1]=((valH<<2)|(valL>>6));
      resp[2]=(valL<<2);
      resp[3]=CRC8((((uint32_t)resp[0])<<24)|(((uint32_t)resp[1])<<16)|(((uint32_t)resp[2])<<8));
      write(uart1, resp, sizeof(resp));
      ctr2+=mov2;
     }

}
return 0;
}

void aFunction(int gpio, int level, uint32_t tick)
{
   clock_gettime (CLOCK_REALTIME, &mt2);
   tt=1000000000*(mt2.tv_sec - mt1.tv_sec)+(mt2.tv_nsec - mt1.tv_nsec);
   //printf("Time us:%ld\n", tt/1000);
   flag=1;

}

