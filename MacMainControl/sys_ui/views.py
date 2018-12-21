from django.http import HttpResponse
from .models import SysUIScript
from django.shortcuts import render
import os

# Create your views here.
def index(request):
    script_list = SysUIScript.objects.filter(name__startswith='sysui')
    context = {
        'script_list': script_list
    }
    return HttpResponse(render(request, 'sys_ui/index.html', context))


def get_content(request, script_id):
    script_name = SysUIScript.objects.get(id=script_id).name
    script_path = SysUIScript.objects.get(id=script_id).path
    filename = script_path + script_name

    script_content = SysUIScript().read_script(filename)
    return HttpResponse(script_content)


def list(request):
    script_list = SysUIScript.objects.filter(name__startswith='sysui')
    output = ','.join([q.name for q in script_list])
    return HttpResponse(output)


def execute_script(request, script_id):
    script_name = SysUIScript.objects.get(id=script_id).name
    script_path = SysUIScript.objects.get(id=script_id).path
    filename = script_path + script_name

    print(filename)
    con = filename

    try:
        os.system('osascript ' + con)
        output = "success"
    except 'Exception':
        output = "fail"

    return HttpResponse(output)
