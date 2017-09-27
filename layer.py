import os, subprocess, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause
allowedPersons=['62856313xxxx'] #Filter the senders numbers with country code without +
ap = set(allowedPersons)

name = "Whatsapp Name"
filelog = "/root/.yowsup/Not allowed.log"

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.5)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            time.sleep(2)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            time.sleep(1)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(3)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = messageProtocolEntity.getBody().lower()
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity


        if messageProtocolEntity.getFrom(False) in ap:
            if message == 'apa yang bisa kamu lakukan':
                answer = "Hai "+namemitt+"\n\nKamu bisa tanyakan sesuatu ke saya:\n\nTinggi air\nStatus"
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'tinggi air' or  'status':
                GPIO.setmode(GPIO.BCM)
                TRIG = 23 
                ECHO = 24
                print "Progres Pengukuran Ketinggian Air"
                GPIO.setup(TRIG,GPIO.OUT)
                GPIO.setup(ECHO,GPIO.IN)
                GPIO.output(TRIG, False)
                print "Menunggu Proses Sensor"
                time.sleep(2)
                GPIO.output(TRIG, True)
                time.sleep(0.00001)
                GPIO.output(TRIG, False)
                while GPIO.input(ECHO)==0:
                  pulse_start = time.time()
                while GPIO.input(ECHO)==1:
                  pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                tinggi_air = 150 - distance
                if (tinggi_air>100):
                	status='Area Tidak Aman !!!\nSegera Tinggalkan Area Sungai'
                else:
                	status='Area Aman :D' 
                print "Ketinggian Air:",tinggi_air,"cm"
                GPIO.cleanup()
                if (message=='tinggi air'):		
                	answer = 'Ketinggian Air Sungai %fcm'%tinggi_air
                elif (message=='status'):
                	answer = status
                else:
                        answer = "Maaf "+namemitt+", Saya tidak mengerti yang kamu tanyakan.\n Coba : 'apa yang bisa kamu lakukan'"
                self.toLower(textmsg(answer,to=recipient))
                print answer
		
            else:
                jawab = "Maaf "+namemitt+", Saya tidak mengerti yang kamu tanyakan.\n Coba : 'apa yang bisa kamu lakukan'"
                self.toLower(textmsg(jawab, to = recipient ))
                print jawab
                

        else:
            answer = "Hai "+namemitt+", Maaf, kamu tidak terdaftar.\nSilahkan follow sosial media\nTwitter : @plhorizz\nFacebook : Achmad devilbat al hasan"
            time.sleep(20)
            self.toLower(textmsg(answer, to = recipient))
            print answer
            out_file = open(filelog,"a")
            out_file.write("------------------------"+"\n"+"Sender:"+"\n"+namemitt+"\n"+"Number sender:"+"\n"+recipient+"\n"+"Message text:"+"\n"+message+"\n"+"------------------------"+"\n"+"\n")
            out_file.close()
