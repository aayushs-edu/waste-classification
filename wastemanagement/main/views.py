from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from main.camera import *

# Create your views here.
def index(response):
    return render(response, "main/base.html", {})

def recycle(response):
    return render(response, "main/recycle.html", {})

@gzip.gzip_page
def camera(request):
    return HttpResponse(print(request.user.get_all_permissions()))
    """
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'err_cam.html')
    """
