import sys,datetime,os
from twython import Twython
CONSUMER_KEY = 'vpAWlpzZtW2Q6TewsgYkFxxxx'                              # Replace your Consumer key
CONSUMER_SECRET = 'V677rvSv4fMwntu8BvUSHlVvVu960ChBuG5Xq6uhDs21Cbxxxx'  # Replace your Consumer secret
ACCESS_KEY = '275364227-JhD1qE6X6uT61bYRbQ6CGr2qK1DXoeKnSHaRxxxx'       # Replace your Access key
ACCESS_SECRET = 'mcXKf4ns8EdBpRu5MHBf7p4dumZnKbqC1CMlw2681xxxx'         # Replace your Access secret
api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIG = 23 
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
while(True):
        tim=datetime.datetime.now()
        GPIO.output(TRIG, False)
        print "Menunggu Proses Sensor"
        time.sleep(3600)
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
        tinggi_air = round(tinggi_air)
        if (tinggi_air>100):
                kondisi='Area Tidak Aman !!!\nSegera Tinggalkan Area Sungai Dusun Bendungan'
        else:
                kondisi='Area Aman :D'
        print(tinggi_air)
        api.update_status(status= 'Status = '+kondisi+'\nKetinggian Air Sungai Dusun Bendungan= %dcm\nPada %s #fb'%(tinggi_air,tim))
GPIO.cleanup()
