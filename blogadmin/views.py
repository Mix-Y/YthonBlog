from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from . import models
from django.contrib.auth.models import ContentType, Permission


def admin(request):
    user = request.user
    if 'admin.add_logentry' not in user.get_all_permissions():
        return HttpResponseRedirect('/accounts/login/')

    return render(request, 'blog/home.html')
