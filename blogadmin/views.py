from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth.models import ContentType, Permission
import json
import demjson
from blog import models


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
    return render(request, 'blogadmin/home.html', dic)


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
    return render(request, 'blogadmin/emailset.html', dic)


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


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminNavSet(request):
    dic = {'title': '版块管理', 'navs': models.Section.objects.all(), 'lownavs': models.SectionTree.objects.all()}
    getsetting(dic)
    if request.method == 'POST':

        img = request.FILES.get('navimg')
        name = request.POST['navname']
        desc = request.POST['navdesc']
        key = request.POST['key']
        if key != "0":
            pid = models.Section.objects.get(name=key)
            num = pid.TreeSum + 1
            models.SectionTree.objects.create(name=name, Section=pid, describe=desc, image=img)
            models.Section.objects.filter(name=key).update(TreeSum=num)
        else:
            models.Section.objects.create(name=name, TreeSum=0, describe=desc, image=img)
    return render(request, 'blogadmin/navset.html', dic)


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminNavRevise(request):
    dic = {'title': '版块修改'}
    getsetting(dic)
    if request.method == 'POST':
        img = request.FILES.get('navimg')
        navname = request.POST['navname']
        desc = request.POST['navdesc']
        name = request.POST['pk']
        if request.POST['method'] == '1':
            models.Section.objects.filter(id=name).update(name=navname, describe=desc, image=img)
        elif request.POST['method'] == '4':
            models.SectionTree.objects.filter(id=name).update(name=navname, describe=desc, image=img)
        return HttpResponseRedirect('/admin/navset/')
    if request.method == 'GET':
        name = int(request.GET['name'])
        method = request.GET['method']
        if method == '3':
            models.Section.objects.filter(id=name).delete()
            return HttpResponseRedirect('/admin/navset/')
        elif method == '2':
            models.SectionTree.objects.filter(id=name).delete()
            return HttpResponseRedirect('/admin/navset/')
        elif method == '1':
            dic['data'] = models.Section.objects.get(id=name)
            dic['method'] = '1'
            return render(request, 'blogadmin/navrevise.html', dic)
        elif method == '4':
            dic['method'] = '4'
            dic['data'] = models.SectionTree.objects.get(id=name)
            return render(request, 'blogadmin/navrevise.html', dic)
