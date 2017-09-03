import json
import os
import random
import signal
import string

import time
import zipfile

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from web import models
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from web.libs import task_handler
from wsgiref.util import FileWrapper  # from django.core.servers.basehttp import FileWrapper

# Create your views here.


def index(request):
    return render(request, 'index.html')


def acc_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or '/')
        else:
            error = 'Wrong username or password'
    return render(request, 'login.html', locals())


def host_list(request):
    return render(request, 'host_list.html')


def get_host_list(request):
    group_id = request.GET.get('group_id')
    if group_id:
        group_id = int(group_id)
        # -1 未分组
        if group_id == -1:
            host_list = list(request.user.bind_host_users.values('host__ip_addr', 'id', 'host__hostname', 'host__port',
                                                                 'host_user__username'))
        else:
            group_obj = request.user.host_groups.get(id=group_id)
            host_list = list(group_obj.bind_host_users.values('host__ip_addr', 'id', 'host__hostname', 'host__port',
                                                              'host_user__username'))
        return HttpResponse(json.dumps(host_list))


def get_token(request):
    bind_host_id = request.GET.get('bind_host_id')
    token_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
    token_obj = models.Token.objects.create(account=request.user, bind_host_user_id=bind_host_id, val=token_str)
    return HttpResponse(json.dumps({'token': token_obj.val}))


def multi_cmd(request):
    return render(request, 'multitask_cmd_bak.html')


def multitask(request):
    task_obj = task_handler.Task(request)
    if task_obj.is_valid():
        res = task_obj.run()
        return HttpResponse(json.dumps({'task_id': res.id, 'timeout': res.timeout}))
    else:
        return HttpResponse(json.dumps(task_obj.errors))


def multitask_result(request):
    task_id = request.GET.get('task_id')
    if task_id:
        task_obj = models.Task.objects.get(id=task_id)
        task_result = list(task_obj.tasklog_set.values('id', 'status', 'bind_host__host__ip_addr',
                                                       'bind_host__host__hostname', 'result', 'date'))
        # default下面是一个函数 是处理json不能转换的数据类型
        return HttpResponse(json.dumps(task_result, default=date_handler))


def date_handler(val):
    return time.strftime("%Y-%m-%d %H:%M:%S", val.timetuple())


def terminate_task(request):

    task_id = request.POST.get('task_id')
    task_obj = models.Task.objects.get(id=task_id)
    # 杀掉父进程及关联的子进程
    os.killpg(task_obj.pid, signal.SIGTERM)
    return HttpResponse(json.dumps({'status': 0, 'msg': 'task got killed'}))


def multi_file(request):
    random_tag = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
    return render(request, 'multitask_file.html', locals())


@csrf_exempt
def file_upload(request):
    random_tag = request.GET.get('random_tag')
    # 每个用户每次上传文件存放的路径
    upload_dir = "uploads/%s/%s" % (request.user.id, random_tag)
    if not os.path.isdir(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)

    file_obj = request.FILES.get('file')
    new_file = open("%s/%s" % (upload_dir, file_obj.name), 'wb')
    for trunk in file_obj.chunks():
        new_file.write(trunk)
    new_file.close()
    return HttpResponse(json.dumps({'status': 0}))


def send_zipfile(request, task_id, file_path):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    zip_file_name = 'task_id_%s_files' % task_id
    archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write('%s/%s' % (file_path, filename), arcname=filename)
    archive.close()
    wrapper = FileWrapper(open(zip_file_name, 'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
    response['Content-Length'] = os.path.getsize(zip_file_name)
    # temp.seek(0)
    return response


def download_task_file(request):
    task_id = request.GET.get('task_id')
    filepath = "%s/%s" % (settings.DOWNLOADS_DIR, task_id)
    # 返回zip包
    return send_zipfile(request, task_id, filepath)



