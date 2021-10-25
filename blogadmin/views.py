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
    dic = {'title': '版块管理', 'navs': models.Section.objects.all()}
    getsetting(dic)
    if request.method == 'POST':

        img = request.FILES.get('navimg')
        name = request.POST['navname']
        desc = request.POST['navdesc']
        key = request.POST['key']
        models.Section.objects.create(name=name, TreeSum=0, describe=desc, image=img, parent=key)
        if key != 0:
            f = models.Section.objects.get(id=key)
            n = f.TreeSum + 1
            models.Section.objects.filter(id=key).update(TreeSum=n)
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
        return HttpResponseRedirect('/admin/navset/')
    if request.method == 'GET':
        name = int(request.GET['name'])
        method = request.GET['method']
        if method == '5':
            models.ArticleSystem.objects.filter(id=name).delete()
            return HttpResponseRedirect('/admin/articlesy/')
        if method == '3':
            models.Section.objects.filter(id=name).delete()
            return HttpResponseRedirect('/admin/navset/')
        elif method == '1':
            dic['data'] = models.Section.objects.get(id=name)
            dic['method'] = '1'
            return render(request, 'blogadmin/navrevise.html', dic)


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminArticleSy(request):
    dic = {'title': '文章分类'}
    getsetting(dic)
    dic['data'] = models.ArticleSystem.objects.all()
    dic['data2'] = models.Section.objects.all()
    dic['parent'] = 0
    dic['last'] = models.ArticleSystem.objects.last()
    if request.method == 'POST':
        try:
            key = request.POST['key']
            name = request.POST['name']
            section = request.POST['section']
            if key == "none":
                models.ArticleSystem.objects.create(name=name, parent=0, sum=0, section=section)
            else:
                f = models.ArticleSystem.objects.get(id=key)
                n = int(f.sum) + 1
                n2 = int(f.level) + 1
                models.ArticleSystem.objects.filter(id=key).update(sum=n)
                models.ArticleSystem.objects.create(name=name, parent=key, sum=0, section=section, level=n2)
        except:
            key = request.POST['rekey']
            name = request.POST['rename']
            models.ArticleSystem.objects.filter(id=key).update(name=name)
    return render(request, 'blogadmin/articlesy.html', dic)

@permission_required('admin.add_logentry', login_url='/accounts/login/')
def adminTimeMess(request):
    dic = {'title': '时间杂记'}
    getsetting(dic)
    if request.method == 'POST':
        dic['TIME_BOX_NAME'] = request.POST['TIME_BOX_NAME']
        dic['TIME_BOX_DESC'] = request.POST['TIME_BOX_DESC']
        body = request.POST['body']
        if body == '0':
            writeSet(dic)
        else:
            writer = str(request.user)
            models.TimeMess.objects.create(body=body, writer=writer)
    return render(request, 'blogadmin/timebox.html', dic)
