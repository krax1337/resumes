from django.shortcuts import render
from django.http import HttpResponse
from xml.etree import ElementTree as ET
import requests
import urllib
import os
import shutil
from .vacants import get_vacants
# Create your views here.





def home(request):
    return render(request, 'index.htm', {'what':'Upload your CV'})

def upload(request):
    requestURL="https://www.enbek.kz/ru/xml/jooble"
    root = ET.parse(urllib.request.urlopen(requestURL)).getroot()
    s=""
    all_vacants_info=[]
    vacants_ids=[]
    if request.method == 'POST':
        jobs, vacants_ids= handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        for job in root.iter('job'):
            for key in vacants_ids:
                if(job.attrib.get('id') == key):
                    all_vacants_info.append("Название: "+str(job.find('name').text))
                    all_vacants_info.append("Регион: "+str(job.find('region').text))
                    all_vacants_info.append("Зарплата: "+str(job.find('salary').text))
                    all_vacants_info.append("Описание: "+str(job.find('description').text))
                    all_vacants_info.append("Почта: "+str(job.find('email').text))
                    all_vacants_info.append("Телефон: "+str(job.find('phone').text))
                    all_vacants_info.append("Ссылка: "+str(job.find('link').text))
    
    return render(request, 'success.htm', {'vacants':all_vacants_info})

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    dir_path = 'upload/' + filename
    results = []
    results = get_vacants(dir_path)
    if os.path.exists('upload/'):
        shutil.rmtree('upload/')
    return results