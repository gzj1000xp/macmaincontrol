from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import ItunesScript
from django.shortcuts import render
import os


def index(request):
    script_list = ItunesScript.objects.filter(name__startswith='itunes')
    context = {
        'script_list': script_list
    }
    return HttpResponse(render(request, 'itunes/index.html', context))


def get_content(request, script_id):
    script_name = ItunesScript.objects.get(id=script_id).name
    script_path = ItunesScript.objects.get(id=script_id).path
    filename = script_path + script_name

    script_content = ItunesScript().read_script(filename)
    return HttpResponse(script_content)


def list(request):
    script_list = ItunesScript.objects.filter(name__startswith='itunes')
    output = ','.join([q.name for q in script_list])
    return HttpResponse(output)


def execute_script(request, script_id):
    script_name = ItunesScript.objects.get(id=script_id).name
    script_path = ItunesScript.objects.get(id=script_id).path
    filename = script_path + script_name

    print(filename)
    con = filename

    try:
        os.system('osascript ' + con)
        output = "success"
    except 'Exception':
        output = "fail"

    return HttpResponse(output)
