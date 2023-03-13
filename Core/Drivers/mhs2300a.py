import time

import serial
from cached_property import cached_property


class MHS2300: 
    def __init__(self, port_name="COM3"):
        self.port = serial.Serial(port_name, 57600, timeout=0.1)
        #Always turns on both channels
        self.port.write(':01,w611,000\r\n'.encode())
        self.port.write(':01,w621,000\r\n'.encode())
            
        
    Wdict={0:'Sine',1:'Square',2:'Triangle'}
    prefix = {3:'K',6:'M',9:'G'}   
        
    
    @staticmethod
    def Freq(kk):
        kk1="{:e}".format(kk)
        Order=kk1[kk1.find('+')+1:]
        Extra=int(Order)%3
        Real_Order=int(Order)-Extra
        Valor=str(kk/10**Real_Order) 
        try:
            u=prefix[Real_Order]+'Hz'
            Valor= Valor+u
            return Valor
        except: 
            return Valor
    
    @staticmethod   
    def Waveform(self,In):
        try: 
            return(self.Wdict[In])
        except:
            return('Custom')
    
    @staticmethod
    def decodeN(self,s,ch):
        AA=s.split(',')
        #print(int(AA[1][3:]))
        a1=self.Waveform(self,int(AA[1][3:]))
        a2=self.Freq(int(AA[2][3:]))
        a3=str(int(AA[3][3:])/100)
        a4=str(int(AA[4][3:])-100)
        a5=str(int(AA[5][3:])/10)
        a6=str(int(AA[6][3:])/10)
        print('Channel: '+str(ch)+' \n'+'Waveform: '+a1+'\nFrequency: '+a2+'\nAmplitude: '+a3+'V\nOffset: '+a4+' \nDuty:'+a5+' \nPhase: '+a6)

    
    def send(self,command):
        command =':01,'+ command +',000\r\n'
        self.port.write(command.encode())
        data=self.port.readline()    
        data_clean=data.decode().strip()
        return data_clean
    
    def on(self,Channel):
        A=self.send('w6'+str(Channel)+'1')
            
    def off(self,Channel):
        A=self.send('w6'+str(Channel)+'0')  
    
    def Frequency(self,Channel,Value):
        A=self.send('w'+str(22+Channel)+str(int(Value*100)))
                  
    def Amplitude(self,Channel,Value):
        A=self.send('w'+str(24+Channel)+str(int(Value*100)))
    
    def Offset(self,Channel,Value):
        A=self.send('w'+str(26+Channel)+str(int(Value)+100))
                  
    def Duty(self,Channel,Value):
        A=self.send('w'+str(28+Channel)+str(int(Value)*10))

    def Phase(self,Channel,Value):
        A=self.send('w'+str(30+Channel)+str(int(Value)))
    
    def ReadChannel(self,Channel):
        List=[]
        while len(List)!=91:
            if Channel==1:
                List=self.send('r21,r23,r25,r27,r29,r31')
            elif Channel==2:
                List=self.send('r22,r24,r26,r28,r30,r32')         
        print(List)

    
    def ChannelInfo(self,Channel):
        List=[]
        while len(List)!=91:
            if Channel==1:
                List=self.send('r21,r23,r25,r27,r29,r31')
            elif Channel==2:
                List=self.send('r22,r24,r26,r28,r30,r32')
        self.decodeN(self,List,Channel)
