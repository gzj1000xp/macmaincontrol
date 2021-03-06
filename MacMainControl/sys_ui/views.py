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


def insert_script(request):
    filepath = 'scripts/'
    output = []
    num = 0
    SCRIPT_NAME='sysui'
    for filename in os.listdir(filepath):
        if filename.split('_')[0] == SCRIPT_NAME:
            queue = SysUIScript.objects.all()
#            print(queue)
#            print(queue.count())
#            判断现有脚本列表是否为空，空则直接导入，非空判断是否已存在。
            if queue.count() == 0:
                num = num + 1
                SysUIScript.objects.create(name=filename, path=filepath)
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
                    SysUIScript.objects.create(name=filename, path=filepath)
                    output.append('Record ' + str(num) + ' insert success.')
                else:
                    num = num + 1
                    output.append('Script ' + filename + ' already exsists.')
        else:
            output.append('This script does not start as ' + SCRIPT_NAME + '.')
    context = {
        'output': output
    }
    return HttpResponse(render(request, 'sys_ui/insert.html', context))
