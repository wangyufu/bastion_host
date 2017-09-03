"""bastion_host URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/$', views.acc_login),
    url(r'^host_list/$', views.host_list, name='host_list'),
    url(r'^multitask/cmd/$', views.multi_cmd, name='multi_cmd'),
    url(r'^multitask/file/$', views.multi_file, name='multi_file'),
    url(r'^api/host_list/$', views.get_host_list, name='get_host_list'),
    url(r'^api/get_token/$', views.get_token, name='get_token'),
    url(r'^api/multitask/$', views.multitask, name='multitask'),
    url(r'^api/multitask/result/$', views.multitask_result, name='get_task_result'),
    url(r'^api/multitask/stop/$', views.terminate_task, name='stop_task'),
    url(r'^api/multitask/file_upload/$', views.file_upload, name='file_upload'),
    url(r'^api/multitask/file_download/$', views.download_task_file, name='download_task_file'),

]
