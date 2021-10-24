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

           'articles': models.Article.objects.all().order_by('-id')[:9]}
    getsetting(dic)
    return render(request, 'blog/home.html', dic)


def navs(request):
    dic = {'title': '首页', 'page': 'navs', 'navs': models.Section.objects.all(),
           }
    getsetting(dic)
    if request.method == 'GET':
        name = request.GET['page']
        dic['sys'] = models.ArticleSystem.objects.filter(section=name)
        dic['title'] = name
        data = models.Section.objects.get(id=name)
        dic['PageData'] = data
        dic['articles'] = models.Article.objects.filter(section=name).order_by('-id')[:9]
    return render(request, 'blog/nav.html', dic)


def write(request):
    dic = {'title': '写文章', 'page': 'navs', 'navs': models.Section.objects.all(),
            'sys': models.ArticleSystem.objects.all(),
           'last': models.ArticleSystem.objects.last()}
    getsetting(dic)
    if request.method == 'POST':
        name = request.POST['name']
        fname = request.POST['fname']
        key = request.POST['key']
        body = request.POST['body']
        writer = str(request.user)
        if int(key) > 10000:
            key = int(key[4:])
            m = models.ArticleSystem.objects.get(id=key)
            models.Article.objects.create(title=name, ftitle=fname, parent=key, body=body, section=m.section, writer=writer)
        else:
            key = int(key)
            models.Article.objects.create(title=name, ftitle=fname, parent=0, body=body, section=key, writer=writer)
    return render(request, 'article/write.html', dic)
