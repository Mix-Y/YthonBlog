from django.contrib import admin
from blog.models import Setting,  Article, Remark, Section, ArticleSystem

# Register your models here.


admin.site.register([Setting, Article, Remark, Section, ArticleSystem])
