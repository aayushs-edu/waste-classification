from PIL import Image
from imutils.video import VideoStream
import imutils
from ultralytics import YOLO
import cv2,os,urllib.request
import math
import numpy as np
from django.conf import settings
import tensorflow as tf

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
	def __init__(self):
		self.url = "http://192.168.0.100:8080/shot.jpg"

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
	def __init__(self): self.model = YOLO("yolo-Weights/yolov8n.pt");self.vs = VideoStream(src=0).start();self.pause = 0;self.detected=[]; self.waste_disposal_advice = {"person": "Encourage proper disposal of personal items and promote recycling where applicable.", "bicycle": "Donate or sell unwanted bicycles, and recycle parts when needed.", "car": "Recycle old cars through authorized scrap yards to minimize environmental impact.", "motorbike": "Properly dispose of old motorbikes through authorized channels or consider donating.", "aeroplane": "Work with aviation recycling programs for sustainable disposal of retired aircraft.", "bus": "Utilize public transportation agency guidelines for retiring and recycling old buses.", "train": "Follow railway industry guidelines for responsible disposal and recycling practices.", "truck": "Work with auto recycling facilities to properly dispose of old trucks.", "boat": "Consider boat recycling programs or dismantle and recycle components responsibly.", "traffic_light": "Collaborate with local authorities for recycling and upgrading traffic signal systems.", "fire_hydrant": "Coordinate with city services for proper maintenance and recycling of fire hydrants.", "stop_sign": "Work with traffic management agencies to recycle and replace outdated stop signs.", "parking_meter": "Follow municipal guidelines for recycling and disposing of old parking meters.", "bench": "Consider refurbishing or donating old benches before disposal.", "bird": "Focus on habitat preservation and reducing pollution to protect bird populations.", "cat": "Encourage responsible pet ownership and consider adoption for unwanted cats.", "dog": "Promote responsible pet ownership and consider adoption for unwanted dogs.", "horse": "Work with equine rescue organizations for proper care and rehoming of unwanted horses.", "sheep": "Explore options for responsible farming practices and wool recycling.", "cow": "Support sustainable agriculture practices and explore options for responsible disposal.", "elephant": "Advocate for wildlife conservation and ethical treatment of elephants in captivity.", "bear": "Support wildlife preservation efforts and responsible handling of captive bears.", "zebra": "Encourage conservation and ethical management of captive zebras.", "giraffe": "Support wildlife conservation initiatives for the protection of giraffes.", "backpack": "Donate gently used backpacks or recycle worn-out ones through textile recycling programs.", "umbrella": "Recycle broken umbrellas through specialized programs or reuse functional parts.", "handbag": "Donate or sell unwanted handbags, and recycle non-reusable materials.", "tie": "Consider donating ties or repurposing them for creative projects before disposal.", "suitcase": "Recycle or donate suitcases in good condition to extend their life cycle.", "frisbee": "Reuse or donate old frisbees, and recycle them when they are no longer usable.", "skis": "Explore options for donating or recycling old skis to minimize environmental impact.", "snowboard": "Donate or recycle snowboards through specialized programs.", "sports_ball": "Donate or recycle old sports balls through appropriate channels.", "kite": "Repurpose or recycle old kites, and consider eco-friendly alternatives.", "baseball_bat": "Donate used baseball bats or recycle them through sports equipment recycling programs.", "baseball_glove": "Recycle or donate old baseball gloves to promote sustainability.", "skateboard": "Consider donating or recycling old skateboards through skateboard recycling programs.", "surfboard": "Repurpose or recycle old surfboards through specialized programs.", "tennis_racket": "Donate or recycle old tennis rackets through sports equipment recycling initiatives.", "bottle": "Promote recycling of plastic, glass, and metal bottles through local recycling programs.", "wine_glass": "Recycle glass wine glasses through appropriate recycling facilities.", "cup": "Opt for reusable cups whenever possible and recycle disposable cups responsibly.", "fork": "Choose reusable utensils and recycle metal forks when no longer usable.", "knife": "Opt for durable and reusable knives, and recycle metal knives responsibly.", "spoon": "Use reusable spoons and recycle metal spoons when they reach the end of their life.", "bowl": "Choose durable and reusable bowls, and recycle them when necessary.", "banana": "Compost banana peels to reduce organic waste and promote nutrient recycling.", "apple": "Compost apple cores or use them for other sustainable purposes.", "sandwich": "Opt for reusable containers and recycle disposable packaging.", "orange": "Compost orange peels or use them for natural cleaning solutions.", "broccoli": "Compost broccoli stems and leaves to minimize kitchen waste.", "carrot": "Compost carrot peels or use them for homemade vegetable broth.", "hot_dog": "Choose sustainably sourced hot dogs and recycle packaging materials.", "pizza": "Compost pizza boxes or recycle them if they are free of grease and contaminants.", "donut": "Opt for reusable containers and recycle or compost donut packaging.", "cake": "Choose sustainable packaging for cakes and recycle it responsibly.", "chair": "Consider refurbishing or donating old chairs before disposal.", "sofa": "Explore options for donating or recycling old sofas to minimize waste.", "potted_plant": "Compost or recycle potted plants, and consider donating them if still viable.", "bed": "Donate or recycle old beds to promote sustainability.", "dining_table": "Consider refurbishing or donating old dining tables before disposal.", "toilet": "Follow local guidelines for the responsible disposal of old toilets.", "tv_monitor": "Recycle old TV monitors through electronic waste recycling programs.", "laptop": "Recycle or donate old laptops to extend their useful life.", "mouse": "Recycle or donate old computer mice to minimize electronic waste.", "remote": "Recycle or donate old remote controls to reduce electronic waste.", "keyboard": "Recycle or donate old keyboards to minimize electronic waste.", "cell_phone": "Recycle old cell phones through electronic waste recycling programs.", "microwave": "Recycle or donate old microwaves through electronic waste recycling initiatives.", "oven": "Recycle or donate old ovens to minimize electronic waste.", "toaster": "Recycle or donate old toasters to reduce electronic waste.", "sink": "Recycle or donate old sinks responsibly.", "refrigerator": "Recycle or donate old refrigerators to minimize electronic waste.", "book": "Donate or recycle old books through book donation programs or recycling centers.", "clock": "Recycle old clocks through appropriate channels.", "vase": "Donate or recycle old vases to minimize waste.", "scissors": "Recycle or donate old scissors to reduce waste.", "teddy_bear": "Donate gently used teddy bears or recycle them through appropriate channels.", "hair_drier": "Recycle old hair dryers through electronic waste recycling programs.", "toothbrush": "Choose eco-friendly toothbrushes and recycle old ones through designated programs."}


	def __del__(self):
		cv2.destroyAllWindows()
  
	def get_frame(self):
		frame = self.vs.read()
		frame = imutils.resize(frame, width=650)
		frame = cv2.flip(frame, 1)
		print(frame)
		# detect faces in the frame and determine if they are wearing a
		# face mask or not
  
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
				print("monkey", frame[x1:x2, y1:y2].shape, x1, y1, x2, y2)
				print(frame[x1:x2, y1:y2])

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

				if confidence > 0.65:
					self.detected.append(classNames[cls])
					cv2.putText(frame, self.map_adv(classNames[cls]) + f" {confidence}", org, font, fontScale, (76,186,111), thickness)
					cv2.rectangle(frame, (x1, y1), (x2, y2), (76,186,111), 3)

		# loop over the detected face locations and their corresponding
		# locations
		ret, jpeg = cv2.imencode('.jpg', frame)
		return jpeg.tobytes()

	def map_adv(self, det):
		return self.waste_disposal_advice[det]
  
        
		
class LiveWebCam(object):
	def __init__(self):pass

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		success,imgNp = self.url.read()
		resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR) 
		ret, jpeg = cv2.imencode('.jpg', resize)
		return jpeg.tobytes()