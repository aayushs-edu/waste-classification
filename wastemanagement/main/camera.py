from PIL import Image
from imutils.video import VideoStream
import imutils
from ultralytics import YOLO
import cv2,os,urllib.request
from pathlib import Path
import math
import numpy as np
from django.conf import settings

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
  
        
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()


class IPWebCam(object):
	def __init__(self): pass
		#self.url = "http://192.168.0.100:8080/shot.jpg"

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		imgResp = urllib.request.urlopen(self.url)
		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
		img= cv2.imdecode(imgNp,-1)
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		resize = cv2.resize(img, (640, 480), interpolation = cv2.INTER_LINEAR) 
		frame_flip = cv2.flip(resize,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()


class MaskDetect(object):
	def __init__(self): self.model = YOLO("yolo-Weights/yolov8n.pt");self.vs = VideoStream(src=0).start();


	def __del__(self):
		cv2.destroyAllWindows()
  
	def get_frame(self):
		frame = self.vs.read()
		frame = imutils.resize(frame, width=650)
		frame = cv2.flip(frame, 1)
  
		# object classes
		classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
					"traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
					"dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
					"handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
					"baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
					"fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
					"carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
					"diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
					"microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
					"teddy bear", "hair drier", "toothbrush",
								]; results = self.model(frame, stream=True)
		# coordinates
		for r in results:
			self.detected = []
			boxes = r.boxes

			for box in boxes:
				# bounding box
				x1, y1, x2, y2 = box.xyxy[0]
				x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

				# put box in cam

				# confidence
				confidence = math.ceil((box.conf[0]*100))/100

				# class name
				cls = int(box.cls[0])

				# object details
				org = [x1, y1]
				font = cv2.FONT_HERSHEY_SIMPLEX
				fontScale = 1
				color = (76,186,111)
				thickness = 2

				if confidence > 0.4 and cls != 0:
					cv2.putText(frame, classNames[cls], org, font, fontScale, (76,186,111), thickness)
					cv2.rectangle(frame, (x1, y1), (x2, y2), (76,186,111), 3)

		# loop over the detected face locations and their corresponding
		# locations
		ret, jpeg = cv2.imencode('.jpg', frame)
		return jpeg.tobytes()
  
        
		
class LiveWebCam(object):
	def __init__(self):pass

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		success,imgNp = self.url.read()
		resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR) 
		ret, jpeg = cv2.imencode('.jpg', resize)
		return jpeg.tobytes()