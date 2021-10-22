from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import models


# Create your views here.


def home(request):
    dic = {'page': 'home', 'navs': models.Section.objects.all(), 'lownavs': models.SectionTree.objects.all(),
           'articles': models.Article.objects.all().order_by('-id')[:9]}
    return render(request, 'blog/home.html', dic)


def navs(request):
    dic = {'page': 'navs', 'navs': models.Section.objects.all(), 'lownavs': models.SectionTree.objects.all()}
    if request.method == 'GET':
        name = request.GET['page']
        level = request.GET['level']
        if level == "1":
            data = models.SectionTree.objects.get(name=name)
        else:
            data = models.Section.objects.get(name=name)
        dic['PageData'] = data
        dic['articles'] = models.Article.objects.filter(parent=name).order_by('-id')[:9]
    return render(request, 'blog/nav.html', dic)
