from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'home.html')

def explore(request):
    return render(request,'explore.html')   
def videos(request):
    return render(request,'video.html')    

