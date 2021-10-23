from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogadmin, name='admin'),
    path('siteinf/', views.adminSiteInf, name='SiteInf'),
    path('emailset/', views.adminEmailSet, name='EmailSet'),
    path('loginset/', views.adminLoginSet, name='LoginSet'),
]
