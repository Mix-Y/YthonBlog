from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import models
import json
import math


def getsetting(dic):
    f = open('static/setting/setting.json', 'r')
    data = f.read()
    data = json.loads(data)
    dic.update(data)
    f.close()


# Create your views here.


def home(request):
    dic = {'title': '首页', 'page': 'home', 'navs': models.Section.objects.all(),
           'articles': models.Article.objects.all().order_by('-id')[:9], 'timemess': models.TimeMess.objects.last()}
    getsetting(dic)
    return render(request, 'blog/home.html', dic)


def navs(request):
    dic = {'title': '首页', 'page': 'navs', 'navs': models.Section.objects.all(),
           }

    getsetting(dic)
    if request.method == 'GET':
        name = request.GET['name']
        dic['nownav'] = name
        page = request.GET['page']
        page = int(page)
        left = 9 * page - 9
        right = 9 * page
        dic['last'] = models.ArticleSystem.objects.last()
        dic['sys'] = models.ArticleSystem.objects.filter(section=name)
        dic['title'] = name
        data = models.Section.objects.get(id=name)
        dic['PageData'] = data
        dic['articles'] = models.Article.objects.filter(section=name).order_by('-id')[left:right]
        dic['datas'] = models.Article.objects.filter(section=name)
        lis = []
        for i in range(int(math.ceil(len(dic['datas']) / 9))):
            lis.append(i + 1)
        dic['pages'] = lis
        print(lis)
        n = 2
        if len(lis) > 0:
            if page - lis[0] < 2: n = page - lis[0]
            if abs(page - lis[-1]) == 0: n = 4
            if page - lis[-1] == -1: n = 3
            dic['pagenumr'] = lis[-1]
            dic['pagenum'] = page - n
            dic['pagenumk'] = page
        else:
            dic['pagenumr'] = 1
            dic['pagenum'] = 1
            dic['pagenumk'] = 1
    return render(request, 'blog/nav.html', dic)


def write(request):
    dic = {'title2': '写文章', 'page': 'navs', 'navs': models.Section.objects.all(),
           'sys': models.ArticleSystem.objects.all(),
           'last': models.ArticleSystem.objects.last()}
    getsetting(dic)
    if request.method == 'POST':
        name = request.POST['name']
        fname = request.POST['fname']
        key = request.POST['key']
        body = request.POST['body']
        writer = str(request.user)
        img = request.FILES.get('navimg')
        if int(key) > 10000:
            key = int(key[4:])
            m = models.ArticleSystem.objects.get(id=key)
            models.Article.objects.create(title=name, ftitle=fname, parent=key, body=body, section=m.section,
                                          writer=writer,image=img)
        else:
            key = int(key)
            models.Article.objects.create(title=name, ftitle=fname, parent=0, body=body, section=key, writer=writer,image=img)
    return render(request, 'article/write.html', dic)


def article(request):
    uid = request.GET['id']
    data = models.Article.objects.get(id=uid)
    dic = {'title2': data.title, 'page': 'navs', 'navs': models.Section.objects.all(), }
    getsetting(dic)
    uid = request.GET['id']
    dic['data'] = data
    return render(request, 'article/home.html', dic)
