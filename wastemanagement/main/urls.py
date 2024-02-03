from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('recycle', views.recycle, name="recycle"),
    path('camera', views.camera, name='camera')
]