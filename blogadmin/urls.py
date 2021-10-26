from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogadmin, name='admin'),
    path('siteinf/', views.adminSiteInf, name='SiteInf'),
    path('emailset/', views.adminEmailSet, name='EmailSet'),
    path('loginset/', views.adminLoginSet, name='LoginSet'),
    path('navset/', views.adminNavSet, name='NavSet'),
    path('navset/revise/', views.adminNavRevise, name='NavRevise'),
    path('articlesy/', views.adminArticleSy, name='ArticleSy'),
    path('timemess/', views.adminTimeMess, name='TimeMess'),
    path('homeimage/', views.adminhomeimage, name='homeimage'),
    path('rearticles/', views.adminrearticles, name='rearticles'),
]
