from transform import four_point_transform
import cv2
import numpy as np
import math
from picamera2 import Picamera2, Preview
from time import sleep
import RPi.GPIO as GPIO
import time
import os
from gpiozero import LED
from gpiozero import PWMLED
from gpiozero import Button
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# pins of the stepper motor
out1 = 27
out2 = 17
out3 = 22
out4 = 18

# additional GPIO pins
button = Button(25)
ledR = PWMLED(24)
ledG = LED(23)

# placeholder variable to track status of stepper motor
i=0

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

#vertex class
class vertex:
	def __init__(self, x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def write(self):
		return "v " + str(self.x) + " " + str(self.y) + " " +str(self.z)
		#return  str(self.x) + "," + str(self.y) + "," +str(self.z)
#face class
class face:
	def __init__(self, v1,v2,v3):
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3

	def write(self):
		return "f " + str(self.v1) + " " + str(self.v2) + " " +str(self.v3)

# transforms cylindrical coordinates into rectangular coordinates
def getVertex(pCoord):
	#pass
	H = pCoord.x
	t = pCoord.y
	d = pCoord.z
	if(t>90):
	  x = d*math.cos(t) + 180
	  y = d*math.sin(t) + 180
	  z = H
	elif(t>270):
	  x = d*math.cos(t) + 360
	  y = d*math.sin(t) + 360
	  z = H
	else:
	  x = d*math.cos(t)
	  y = d*math.sin(t)
	  z = H
	return vertex(int(x),int(y),int(z))

# steps motor forward indicated number of steps
# inputs x: number of steps to move, i: status of stepper
# outputs new i (status of stepper)
def step(x, i):
    positive=0
    negative=0
    y=0

    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    #x = input()
    if x>0 and x<=400:
      #print "step"
      for y in range(x,0,-1):
        if negative==1:
          if i==7:
            i=0
          else:
            i=i+1
          y=y+2
          negative=0
        positive=1
        #print((x+1)-y)
        if i==0:
          GPIO.output(out1,GPIO.HIGH)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==1:
          GPIO.output(out1,GPIO.HIGH)
          GPIO.output(out2,GPIO.HIGH)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==2:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.HIGH)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==3:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.HIGH)
          GPIO.output(out3,GPIO.HIGH)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==4:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.HIGH)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==5:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.HIGH)
          GPIO.output(out4,GPIO.HIGH)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==6:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.HIGH)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==7:
          GPIO.output(out1,GPIO.HIGH)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.HIGH)
          time.sleep(0.01)
          #time.sleep(1)
        if i==7:
          i=0
          continue
        i=i+1


    elif x<0 and x>=-400:
      x=x*-1
      for y in range(x,0,-1):
        if positive==1:
          if i==0:
            i=7
          else:
            i=i-1
          y=y+3
          positive=0
        negative=1
        #print((x+1)-y)
        if i==0:
          GPIO.output(out1,GPIO.HIGH)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==1:
          GPIO.output(out1,GPIO.HIGH)
          GPIO.output(out2,GPIO.HIGH)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==2:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.HIGH)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==3:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.HIGH)
          GPIO.output(out3,GPIO.HIGH)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==4:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.HIGH)
          GPIO.output(out4,GPIO.LOW)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==5:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.HIGH)
          GPIO.output(out4,GPIO.HIGH)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==6:
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.HIGH)
          time.sleep(0.01)
          #time.sleep(1)
        elif i==7:
          GPIO.output(out1,GPIO.HIGH)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.HIGH)
          time.sleep(0.01)
          #time.sleep(1)
        if i==0:
          i=7
          continue
        i=i-1

    return i

#turn on green status light
ledG.on()
    
while (1):
	# angular resolution
	numItt = 40

	# angle
	theta = 0
	thetaInc = 360.0/numItt

	# motor position
	motorPos = 0
	motorPosI = 400.0/numItt

	#data
	meshPoints = []
	lineLenth = []

	# while loop for system


	# wait for start button
	while (not button.is_pressed):
		sleep(0.1)

	# turn off/on status light
	ledG.off()
	ledR.pulse()

	while(theta < 360):
		#will loop this
		camera = Picamera2()
		camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
		camera.configure(camera_config)
		#camera.start_preview(Preview.QTGL)
		camera.start()
		#sleep(1)
		camera.capture_file('lineDetection.jpg')
		camera.close()
		img = cv2.imread('lineDetection.jpg')

		#---------- Preview the picture ----------------
		#cv2.imshow("perspective", img)
		#cv2.waitKey(0)

		#get perspective
		tlp = (490.0,0.0)
		trp = (1200.0,0.0)
		brp = (1200.0,840.0)
		blp = (490.0,1030.0)
		pts = np.array([tlp,trp,brp,blp])
		img = four_point_transform(img, pts)

		#---------- Preview the PERSPECTIVE picture ----------------
		#cv2.imshow("perspective", img)
		#cv2.waitKey(0)


		# filter
		lowerb = np.array([125, 0, 0])
		upperb = np.array([255, 255, 255])
		#1200,1600
		red_line = cv2.inRange(img, lowerb, upperb)
		##red_line = cv2.resize(red_line, (60,80), interpolation = cv2.INTER_AREA)


		#---------- Preview the filtered picture ----------------
		#cv2.imshow("perspective", red_line)
		#cv2.waitKey(0)
		#print red_line.shape


		h,w = np.shape(red_line)
		backG = np.zeros((h, w))

		#print backG

		bottomR = 0

		r = 0
		for cIndex in np.argmax(red_line, axis=1):
			if red_line[r,cIndex] != 0:
				backG[r,cIndex] = 1
				bottomR = r
			r += 1

		#---------- Preview the processed picture ----------------
		#cv2.imshow("perspective", backG)
		#cv2.waitKey(0)


		tempV = []
		r = 0
		centerC = backG.shape[1] // 2 #center column
		for cIndex in np.argmax(backG,axis=1):
			if(backG[r,cIndex] == 1):
				#intvi = 0
				H = r-bottomR
				dist = cIndex - centerC
				coord = vertex(H,np.radians(theta),dist)
				tempV.append(coord)
			r += 1
	      
		
		# vertical resolution
		intv = 10
		intv = len(tempV)/intv

		if(len(tempV) != 0 and intv != 0):
			V = []
			V.append(tempV[0])

			for ind in range(1,len(tempV)-2):
				#if(ind % intv == 0):
				V.append(tempV[ind])

			V.append(tempV[(len(tempV)-1)])
			meshPoints.append(V)
			print((str(len(V))))
			lineLenth.append(-1*len(V))

		theta += thetaInc
		i = step(int(motorPosI),i)
		time.sleep(0.1)


	#for row in meshPoints:
	  #for coord in row:
	    #print(getVertex(coord).write())


	shortest = len(meshPoints[np.argmax(lineLenth)])
	print(shortest)

	for line in meshPoints:
		while(len(line) > shortest):
			line.pop(len(line)-2)


	points = []
	faces = []
	firstRow = []
	prevRow = []
	for index in range(1,len(meshPoints[0])+1):

		points.append(getVertex(meshPoints[0][index-1]))
		firstRow.append(index)

	prevRow = firstRow
	for col in range(0,len(meshPoints)):
		if col != 0:
			indexS = prevRow[-1]
			currentRow = []
			for point in range(0,len(meshPoints[col])-1):
				tl = indexS + point + 1
				bl = tl + 1
				tr = prevRow[point]
				br = prevRow[point + 1]

				f1 = face(tl,tr,bl)
				f2 = face(bl,tr,br)
				faces.append(f1)
				faces.append(f2)

				points.append(getVertex(meshPoints[col][point]))
				currentRow.append(tl)
				if(point == len(meshPoints[col])-2):
					points.append(getVertex(meshPoints[col][point+1]))
					currentRow.append(bl)

				if col == (len(meshPoints)-1):
					tr = tl
					br = bl
					tl = firstRow[point]
					bl = firstRow[point+1]
					f1 = face(tl,tr,bl)
					f2 = face(bl,tr,br)
					faces.append(f1)
					faces.append(f2)
			prevRow = currentRow

	#---------- debugging prints ----------------
	#for point in points:
	  #print(point.write())
	#for face in faces:
	  #print(face.write())

	# writing the file
	filetowrite='3d.obj'
	with open(filetowrite, 'w') as file:
		for point in points:
			file.write(point.write() + "\n")
		for f in faces:
			file.write(f.write() + "\n")
		file.close()


	email_user = 'dinicmilutin00@gmail.com'
	email_password = 'oriqqvfrptordbde'
	email_send = 'milutin.dinic@elfak.rs'

	subject = '3D Objekat!'

	msg = MIMEMultipart()
	msg['From'] = email_user
	msg['To'] = email_send
	msg['Subject'] = subject

	body = 'Vas 3d objekat!'
	msg.attach(MIMEText(body,'plain'))

	filename='3d.obj'
	attachment  =open(filename,'rb')

	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename= "+filename)

	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email_user,email_password)


	server.sendmail(email_user,email_send,text)
	server.quit()


	# turn status light off
	ledR.off()
	ledG.on()

	# TODO: send data online
	# TODO: clear variables

GPIO.cleanup()

