from django.shortcuts import render
import os

def index(request):
    return render(request, 'mpassidLogin/index.html')

def redirect(request):
    return render(request, os.getenv('REDIRECT_URL'))