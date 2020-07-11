from django.urls import path 
from . import views

urlpatterns = [
    path("",views.index,name="Home"),
    path("explore",views.explore,name="explore"),
    path("video",views.videos,name="video")


]