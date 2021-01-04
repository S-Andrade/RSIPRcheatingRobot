import cv2 as cv
import numpy as np
import sys
import time
import Image
from naoqi import ALProxy
import time
from deepgaze.color_detection import RangeColorDetector

def showNaoImage(IP, PORT):
  #capture frame from robot
  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 2
  colorSpace = 11

  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

  naoImage = camProxy.getImageRemote(videoClient)

  camProxy.unsubscribe(videoClient)

  width = naoImage[0]
  height = naoImage[1]
  image = np.zeros((height, width, 3), np.uint8)

  if naoImage == None:
  	print ('cannot capture.')
  elif naoImage[6] == None:
   	print ('no image data string.')
  else:
    values = map(ord, list(naoImage[6]))
    i = 0
    for y in range(0, height):
        for x in range(0, width):
            image.itemset((y, x, 0), values[i + 0])
            image.itemset((y, x, 1), values[i + 1])
            image.itemset((y, x, 2), values[i + 2])
            i += 3

    cv.imwrite('camImage.png', image)
    cv.imshow("camImage", image)
    # end capture of frame from robot
#cap = cv.VideoCapture(0)
#ret, image = cap.read()
#cap.release()
	img = cv.imread("camImage.png") #Read the image with OpenCV
	hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	lower = np.array([0, 48, 80], dtype = "uint8")
	upper = np.array([20, 255, 255], dtype = "uint8")
	skinRegionHSV = cv.inRange(hsvim, lower, upper)
	blurred = cv.blur(skinRegionHSV, (2,2))
	ret,thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)
	cv.imwrite("thresh.png", thresh)

	_, contours, _= cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	contours = max(contours, key=lambda x: cv.contourArea(x))
	cv.drawContours(img, [contours], -1, (255,255,0), 2)
	cv.imwrite("contours.png", img)

	hull = cv.convexHull(contours)
	cv.drawContours(img, [hull], -1, (0, 255, 255), 2)
	cv.imwrite("hull.png", img)

	hull = cv.convexHull(contours, returnPoints=False)
	defects = cv.convexityDefects(contours, hull)

	if defects is not None:
  		cnt = 0
	for i in range(defects.shape[0]):  # calculate the angle
  		s, e, f, d = defects[i][0]
  		start = tuple(contours[s][0])
  		end = tuple(contours[e][0])
  		far = tuple(contours[f][0])
  		a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
  		b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
  		c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
  		angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  #      cosine theorem
  		if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
    		cnt += 1
    		cv.circle(img, far, 4, [0, 0, 255], -1)
	if cnt > 0:
  		cnt = cnt+1
	cv.putText(img, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv.LINE_AA)

	cv.imwrite('final_result.png',img)



if __name__ == '__main__':
  IP = "127.0.0.1"
  PORT = 43827

  if len(sys.argv) > 1:
    IP = sys.argv[1]

  naoImage = showNaoImage(IP, PORT)