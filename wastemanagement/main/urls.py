from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('recycle', views.recycle, name="recycle"),
    path('camera', views.camera, name='camera'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('mask_feed', views.mask_feed, name='mask_feed'),
	path('livecam_feed', views.livecam_feed, name='livecam_feed'),
    path('capture_frame/', views.capture_frame, name='capture_frame'),
]