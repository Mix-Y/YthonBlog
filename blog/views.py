from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

from YthonBlog.settings import BASE_DIR
from . import models
import json
import math
from django.db.models import Q


def getsetting(dic):
    f = open('static/setting/setting.json', 'r')
    data = f.read()
    data = json.loads(data)
    dic.update(data)
    f.close()


# Create your views here.


def home(request):
    dic = {'title': '首页', 'page': 'home', 'navs': models.Section.objects.all(),
           'articles': models.Article.objects.all().order_by('-id')[:9], 'timemess': models.TimeMess.objects.last(),
           'mess': models.Remark.objects.all().order_by('-id')[:5], 'messlast': models.Remark.objects.last()}
    getsetting(dic)
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False
    return render(request, 'blog/home.html', dic)


def navs(request):
    dic = {'title': '首页', 'page': 'navs', 'navs': models.Section.objects.all(),
           'mess': models.Remark.objects.all().order_by('-id')[:5], 'messlast': models.Remark.objects.last()}
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False
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


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def write(request):
    dic = {'title2': '写文章', 'page': 'navs', 'navs': models.Section.objects.all(),
           'sys': models.ArticleSystem.objects.all(), 'last': models.ArticleSystem.objects.last(),
           'mess': models.Remark.objects.all().order_by('-id')[:5], 'messlast': models.Remark.objects.last()}
    getsetting(dic)
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False
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
                                          writer=writer, image=img)
        else:
            key = int(key)
            models.Article.objects.create(title=name, ftitle=fname, parent=0, body=body, section=key, writer=writer,
                                          image=img)
    return render(request, 'article/write.html', dic)


def article(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']
        id = request.POST['id']
        models.Remark.objects.create(email=email, writer=name, parent=id, body=body)
    uid = request.GET['id']
    data = models.Article.objects.get(id=uid)
    dic = {'title2': data.title, 'page': 'navs', 'navs': models.Section.objects.all(),
           'remarks': models.Remark.objects.filter(parent=uid), 'data': data,
           'mess': models.Remark.objects.all().order_by('-id')[:5], 'messlast': models.Remark.objects.last()}
    getsetting(dic)
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False
    if request.user.has_perm('blog.change_article'):
        dic['change'] = True
    else:
        dic['change'] = False
    return render(request, 'article/home.html', dic)


def search(request):
    dic = {'title2': '搜索', 'page': 'navs', 'navs': models.Section.objects.all(),
           'mess': models.Remark.objects.all().order_by('-id')[:5], 'messlast': models.Remark.objects.last()}
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False
    getsetting(dic)
    if request.method == 'GET':
        name = request.GET['name']
        dic['articles'] = models.Article.objects.filter(
            Q(title__contains=name) | Q(ftitle__contains=name) | Q(writer__contains=name))
        dic['value'] = name

    return render(request, 'article/search.html', dic)


def mess(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']
        id = request.POST['id']
        models.Remark.objects.create(email=email, writer=name, parent=id, body=body)
    dic = {'title2': '留言', 'page': 'navs', 'navs': models.Section.objects.all(),
           'remarks': models.Remark.objects.filter(parent=0), 'mess': models.Remark.objects.all().order_by('-id')[:5],
           'messlast': models.Remark.objects.last()}
    getsetting(dic)
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False

    return render(request, 'blog/mess.html', dic)


def about(request):
    dic = {'title2': '关于', 'page': 'navs', 'navs': models.Section.objects.all(),
           'mess': models.Remark.objects.all().order_by('-id')[:5],
           'messlast': models.Remark.objects.last()}
    getsetting(dic)
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False

    return render(request, 'blog/about.html', dic)


@permission_required('admin.add_logentry', login_url='/accounts/login/')
def rewrite(request):
    dic = {'title2': '编辑文章', 'page': 'navs', 'navs': models.Section.objects.all(),
           'sys': models.ArticleSystem.objects.all(), 'last': models.ArticleSystem.objects.last(),
           'mess': models.Remark.objects.all().order_by('-id')[:5], 'messlast': models.Remark.objects.last()}
    getsetting(dic)
    if request.user.is_authenticated:
        dic['login'] = True
    else:
        dic['login'] = False
    id = request.GET['id']
    dic['data'] = models.Article.objects.get(id=id)
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        fname = request.POST['fname']
        key = request.POST['key']
        body = request.POST['body']
        body = body[5:]
        body = body[:-6]
        writer = str(request.user)
        img = request.FILES.get('navimg')

        if int(key) > 10000:
            key = int(key[4:])
            m = models.ArticleSystem.objects.get(id=key)
            if img:
                import os
                f = open(os.path.join(BASE_DIR, 'static', 'uploadimg', img.name), 'wb')
                for chunk in img.chunks():
                    f.write(chunk)
                f.close()
                img = "/uploadimg/" + str(img)
                models.Article.objects.filter(id=id).update(title=name, ftitle=fname, parent=key, body=body,
                                                            section=m.section,
                                                            writer=writer, image=img)
            else:
                models.Article.objects.filter(id=id).update(title=name, ftitle=fname, parent=key, body=body,
                                                            section=m.section,
                                                            writer=writer)
        else:
            key = int(key)
            if img:
                import os
                f = open(os.path.join(BASE_DIR, 'static', 'uploadimg', img.name), 'wb')
                for chunk in img.chunks():
                    f.write(chunk)
                f.close()
                img = "/uploadimg/" + str(img)
                models.Article.objects.filter(id=id).update(title=name, ftitle=fname, parent=0, body=body, section=key,
                                                            writer=writer,
                                                            image=img)
            else:
                models.Article.objects.filter(id=id).update(title=name, ftitle=fname, parent=0, body=body, section=key,
                                                            writer=writer)
    return render(request, 'article/rewrite.html', dic)
