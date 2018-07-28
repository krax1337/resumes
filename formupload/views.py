from django.shortcuts import render
from django.http import HttpResponse
from xml.etree import ElementTree as ET
import requests
import urllib
import os
import shutil
from .vacants import get_vacants

cv_summary = dict()

def home(request):
    return render(request, 'index.html', {'what':'Upload your CV'})

def show(request):
    if request.method == 'GET':
        summary="HEER"
        return render(request, 'show.html', {'summary':"бЛА БЛА БЛА"})





def upload(request):
    requestURL="https://www.enbek.kz/ru/xml/jooble"
    root = ET.parse(urllib.request.urlopen(requestURL)).getroot()
    all_vacants_info=[{}]
    # cv_summary=dict()
    vacants_ids=[]
    
    if request.method == 'POST':
        vacants_ids, cv_summary= handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        print(cv_summary)
        for key in vacants_ids:
            for job in root.iter('job'):
                if(job.attrib.get('id') == key):
                    all_vacants_info.append({
                    
                        'job_name': str(job.find('name').text).replace(", ", "",1),
                        'job_region': str(job.find('region').text),
                        "job_salary": str(job.find('salary').text),
                        "job_description": str(job.find('description').text).replace("p&gt;", " ")
                        .replace("li", " ").replace("ul", " ")
                        .replace("/", " ").replace("&gt;", " ")
                        .replace("&lt;", " ").replace("ul&gt;", " ")
                        .replace("/li&gt;", " ").replace("li&gt;", " ")
                        .replace("-&amp;", " ").replace("nbsp;", " ")
                        .replace("&amp;", " ").replace("quot;"," ")
                        .replace("br"," ").replace("strong"," ")
                        .replace("strong"," ").replace("ol"," "),
                        "job_email": str(job.find('email').text),
                        "job_phone": str(job.find('phone').text),
                        "job_link": str(job.find('link').text),
                    
                    })
               
        return render(request, 'success.html', {'vacants':all_vacants_info, 'cv_summary':cv_summary})
    else:
        cv_summary=request.POST.get("cv_summary", cv_summary)
        return render(request, 'show.html', {'cv_summary':cv_summary})

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    dir_path = 'upload/' + filename
    results = []
    results,cv_summary = get_vacants(dir_path)
    if os.path.exists('upload/'):
        shutil.rmtree('upload/')
    return results,cv_summary