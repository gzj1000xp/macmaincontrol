from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import ChromeScript
from django.shortcuts import render
import os


def index(request):
    script_list = ChromeScript.objects.filter(name__startswith='chrome')
    context = {
        'script_list': script_list
    }
    return HttpResponse(render(request, 'chrome/index.html', context))


def get_content(request, script_id):
    script_name = ChromeScript.objects.get(id=script_id).name
    script_path = ChromeScript.objects.get(id=script_id).path
    filename = script_path + script_name

    script_content = ChromeScript().read_script(filename)
    return HttpResponse(script_content)


def list(request):
    script_list = ChromeScript.objects.filter(name__startswith='chrome')
    output = ','.join([q.name for q in script_list])
    return HttpResponse(output)


def execute_script(request, script_id):
    script_name = ChromeScript.objects.get(id=script_id).name
    script_path = ChromeScript.objects.get(id=script_id).path
    filename = script_path + script_name

    print(filename)
    con = filename

#   使用os模块的popen方法来读取命令执行返回值。
    try:
        command = 'osascript -s s ' + con
        output = os.popen(command).readlines()
#        os.system('osascript ' + con)
#        output = "success"
    except 'Exception':
        output = "fail"

    context = {
        'output': output
    }
    return HttpResponse(render(request, 'chrome/execute.html', context))


def insert_script(request):
    filepath = 'scripts/'
    output = []
    num = 0
    SCRIPT_NAME='chrome'
    for filename in os.listdir(filepath):
        if filename.split('_')[0] == SCRIPT_NAME:
            queue = ChromeScript.objects.all()
#            print(queue)
#            print(queue.count())
#            判断现有脚本列表是否为空，空则直接导入，非空判断是否已存在。
            if queue.count() == 0:
                num = num + 1
                ChromeScript.objects.create(name=filename, path=filepath)
                output.append('Record ' + str(num) + ' insert success.')
            else:
                flag = 0
#                循环比对，判断是否已存在。
                for sid in range(queue.count() + 1):
                    try:
                        if queue.get(id=sid).name == filename:
                            flag = flag + 1
                        else:
                            flag = flag
                    except:
                        pass
#                flag为0表示目标不在现在的列表中，执行导入
                if flag == 0:
                    num = num + 1
                    ChromeScript.objects.create(name=filename, path=filepath)
                    output.append('Record ' + str(num) + ' insert success.')
                else:
                    num = num + 1
                    output.append('Script ' + filename + ' already exsists.')
        else:
            output.append('This script does not start as ' + SCRIPT_NAME + '.')
    context = {
        'output': output
    }
    return HttpResponse(render(request, 'chrome/insert.html', context))
