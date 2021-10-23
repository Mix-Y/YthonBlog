from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import models
import json
import demjson


def getsetting(dic):
    f = open('static/setting/setting.json', 'r')
    data = f.read()
    data = json.loads(data)
    dic.update(data)
    f.close()


# Create your views here.


def home(request):
    dic = {'title': '首页', 'page': 'home', 'navs': models.Section.objects.all(),
           'lownavs': models.SectionTree.objects.all(),
           'articles': models.Article.objects.all().order_by('-id')[:9]}
    getsetting(dic)
    return render(request, 'blog/home.html', dic)


def navs(request):
    dic = {'title': '首页', 'page': 'navs', 'navs': models.Section.objects.all(),
           'lownavs': models.SectionTree.objects.all()}
    getsetting(dic)
    if request.method == 'GET':
        name = request.GET['page']
        dic['title'] = name
        level = request.GET['level']
        if level == "1":
            data = models.SectionTree.objects.get(name=name)
        else:
            data = models.Section.objects.get(name=name)
        dic['PageData'] = data
        dic['articles'] = models.Article.objects.filter(parent=name).order_by('-id')[:9]
    return render(request, 'blog/nav.html', dic)
