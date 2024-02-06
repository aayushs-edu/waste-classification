from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from main.camera import VideoCamera, IPWebCam, MaskDetect, LiveWebCam
# from openai import ChatCompletion
# import openai
import cv2
            
# Create your views here.
def index(response):
    return render(response, "main/base.html", {})

def recycle(response):
    return render(response, "main/recycle.html", {})

def camera(request):
    return render(request, 'main/home.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def webcam_feed(request):
	return StreamingHttpResponse(gen(IPWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def mask_feed(request):
	return StreamingHttpResponse(gen(MaskDetect()),
					content_type='multipart/x-mixed-replace; boundary=frame')
					
def livecam_feed(request):
	return StreamingHttpResponse(gen(LiveWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')

cap = cv2.VideoCapture(0)

def capture_frame(request):
    ret, frame = cap.read()
