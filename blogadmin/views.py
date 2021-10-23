from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

from . import models
from django.contrib.auth.models import ContentType, Permission
import json
import demjson


def getsetting(dic):
    f = open('static/setting/setting.json', 'r')
    data = f.read()
    data = json.loads(data)
    dic.update(data)
    f.close()


def writeSet(dic):
    with open('static/setting/setting.json', 'w') as r:
        # 定义为写模式，名称定义为r
        json.dump(dic, r)
        # 将dict写入名称为r的文件中
    r.close()


def truefalse(StrData):
    StrData = str(StrData)
    StrData.lower()
    if StrData == 'true':
        print(StrData)
        return True
    if StrData == "false":
        print(StrData)
        return False
    return False


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def blogadmin(request):
    dic = {'title': '管理后台'}
    return render(request, 'blogadmin/home.html',dic)


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminSiteInf(request):
    dic = {'title': '网站信息'}
    getsetting(dic)
    if request.method == 'POST':
        dic['SITE_NAME'] = request.POST['sitename']
        dic['SITE_DESC'] = request.POST['sitedesc']
        dic['DName'] = request.POST['dname']
        dic['CN_GOV_RECORD_DATA'] = request.POST['recordinf']

        try:
            dic['CN_GOV_RECORD'] = truefalse(request.POST['record'])
        except MultiValueDictKeyError:
            dic['CN_GOV_RECORD'] = False
        writeSet(dic)
    return render(request, 'blogadmin/siteinf.html', dic)


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminEmailSet(request):
    dic = {'title': '邮件设置'}
    getsetting(dic)
    if request.method == 'POST':
        dic['senderName'] = request.POST['senderName']
        dic['youEamil'] = request.POST['youEamil']
        dic['emailPwd'] = request.POST['emailPwd']
        dic['mailHost'] = request.POST['mailHost']
        dic['hostPort'] = int(request.POST['hostPort'])
        writeSet(dic)
    return render(request, 'blogadmin/emailset.html',dic)


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminLoginSet(request):
    dic = {'title': '用户设置'}
    getsetting(dic)
    if request.method == 'POST':
        try:
            dic['LOGOUT_ON_GET'] = truefalse(request.POST['LOGOUT_ON_GET'])
        except MultiValueDictKeyError:
            dic['LOGOUT_ON_GET'] = False
        try:
            dic['EMAIL_REQUIRED'] = truefalse(request.POST['EMAIL_REQUIRED'])
        except MultiValueDictKeyError:
            dic['EMAIL_REQUIRED'] = False
        dic['EMAIL_VERIFICATION'] = request.POST['EMAIL_VERIFICATION']
        dic['EMAIL_CONFIRMATION_EXPIRE_DAYS'] = int(request.POST['EMAIL_CONFIRMATION_EXPIRE_DAYS'])
        dic['LOGIN_ATTEMPTS_LIMIT'] = int(request.POST['LOGIN_ATTEMPTS_LIMIT'])
        dic['LOGIN_ATTEMPTS_TIMEOUT'] = int(request.POST['LOGIN_ATTEMPTS_TIMEOUT'])
        writeSet(dic)
    return render(request, 'blogadmin/loginset.html', dic)
