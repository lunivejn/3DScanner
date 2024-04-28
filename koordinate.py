# import the required library
from picamera2 import Picamera2, Preview
import cv2
from time import sleep

# define a function to display the coordinates of

# of the points clicked on the image
def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
      print(f'({x},{y})')
      
      # put coordinates as text on the image
      cv2.putText(img, f'({x},{y})',(x,y),
      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      
      # draw point on the image
      cv2.circle(img, (x,y), 3, (0,255,255), -1)
 
# read the input image
#camera = PiCamera()
#camera.start_preview()
#sleep(1)
#camera.capture('test.jpg')
#camera.close()
#img = cv2.imread('test.jpg')
camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera.configure(camera_config)
camera.start_preview(Preview.QTGL)
camera.start()
sleep(1)
camera.capture_file('test.jpg')
camera.close()
img = cv2.imread('test.jpg')

# create a window
cv2.namedWindow('Point Coordinates', cv2.WINDOW_KEEPRATIO)
cv2.resizeWindow('Point Coordinates', 500, 500)

# bind the callback function to window
cv2.setMouseCallback('Point Coordinates', click_event)

# display the image
while True:
   cv2.imshow('Point Coordinates',img)
   k = cv2.waitKey(1) & 0xFF
   if k == 27:
      break
cv2.destroyAllWindows()
