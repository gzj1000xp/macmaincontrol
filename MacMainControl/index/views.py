from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import Index


def index(request):
    script_list = Index.objects.filter()
    context = {
        'script_list': script_list
    }
    return HttpResponse(render(request, 'index/index.html', context))
