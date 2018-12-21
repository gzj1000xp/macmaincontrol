from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import FinderScript


def index(request):
    return HttpResponse("Hello, world. You're at the finder index.")


def get_content(request, filename):
    script_content = FinderScript().read_script(filename)
    return HttpResponse(script_content)


def list(request):
    script_list = FinderScript.objects.filter(name__startswith='finder')
    output = ','.join([q.name for q in script_list])
    return HttpResponse(output)
