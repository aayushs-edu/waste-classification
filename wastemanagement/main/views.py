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

"""

def chatbot_view(request):
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        prompts = []

        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Append conversation messages to prompts
        prompts.extend(conversation)

        # Set up and invoke the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key="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"
        )
        
        # Extract chatbot replies from the response

        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})
            print(conversation)

        # Update the conversation in the session
        request.session['conversation'] = conversation

        return render(request, 'main/recycle.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        request.session.clear()
        return render(request, 'main/recycle.html', {'conversation': conversation})


"""