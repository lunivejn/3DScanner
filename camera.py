from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import numpy as np
from transform import four_point_transform

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
	x = d*math.cos(t)
	y = d*math.sin(t)
	z = H
	return vertex(int(x),int(y),int(z))

theta = 0
#camera = PiCamera()
#acmera.start_preview()
#sleep(5)
#camera.capture('/tmp/picture.jpg')
#camera.stop_preview()

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
sleep(1)
picam2.capture_file("test.jpg")
picam2.close()
img = cv2.imread('test.jpg')
#---------- Preview the picture ----------------

#cv2.imshow("perspective1", img)
#cv2.waitKey(0)

#get perspective
tlp = (490.0,0.0)
trp = (1200.0,0.0)
brp = (1200.0,840.0)
blp = (490.0,1030.0)
pts = np.array([tlp,trp,brp,blp])
img = four_point_transform(img, pts)

#---------- Preview the PERSPECTIVE picture ----------------
cv2.imshow("perspective", img)
#cv2.waitKey(0)

# filter
lowerb = np.array([120, 0, 0])
upperb = np.array([255, 255, 255])
#1200,1600

red_line = cv2.inRange(img, lowerb, upperb)
#red_line = cv2.resize(red_line, (500,500), interpolation = cv2.INTER_AREA)
#red_line = cv2.Canny(img,100,200,L2gradient=True)
#---------- Preview the filtered picture ----------------
cv2.imshow("perspective2", red_line)
#cv2.waitKey(0)
#print(red_line.shape)


h,w = np.shape(red_line)
backG = np.zeros((h, w))

#print(h, w)

bottomR = 0

r = 0
for cIndex in np.argmax(red_line, axis=1):
	if red_line[r,cIndex] != 0:
		backG[r,cIndex] = 1
		bottomR = r
	r += 1
#print(backG)
#---------- Preview the processed picture ----------------
cv2.imshow("perspective3", backG)
cv2.waitKey(0)

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
			
#print(tempV)

# vertical resolutio
intv = 20
intv = len(tempV)/intv

if(len(tempV) != 0 and intv != 0):
	V = []
	V.append(tempV[0])
	
	for ind in range(1,len(tempV)-2):
		if(ind % intv == 0):
			V.append(tempV[ind])

	V.append(tempV[(len(tempV)-1)])
	meshPoints.append(V)
	#print((str(len(V))))
	lineLenth.append(-1*len(V))

for row in meshPoints:
	  for coord in row:
	    print(getVertex(coord).write())
