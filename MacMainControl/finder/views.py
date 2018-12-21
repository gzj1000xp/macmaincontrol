from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import FinderScript


def index(request):
    return HttpResponse("Hello, world. You're at the finder index.")


def get_content(request, script_id):
    script_name = FinderScript.objects.get(id=script_id).name
    script_path = FinderScript.objects.get(id=script_id).path
    filename = script_path + script_name

    script_content = FinderScript().read_script(filename)
    return HttpResponse(script_content)


def list(request):
    script_list = FinderScript.objects.filter(name__startswith='finder')
    output = ','.join([q.name for q in script_list])
    return HttpResponse(output)
