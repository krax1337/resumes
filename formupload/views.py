from django.shortcuts import render
from django.http import HttpResponse
import os
import shutil
from .hh_miner_ru import pdf_to_text
# Create your views here.
def home(request):
    return render(request, 'index.htm', {'what':'Django File Upload'})

def upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        return HttpResponse("Successful")

    return HttpResponse("Failed")

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    dir_path = 'upload/' + filename
    results = []
    results = pdf_to_text(dir_path)
    print(results)
    if os.path.exists('upload/'):
        shutil.rmtree('upload/')