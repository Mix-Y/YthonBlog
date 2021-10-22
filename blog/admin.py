from django.contrib import admin
from blog.models import Setting, SectionTree, Article, Remark, Section
# Register your models here.


admin.site.register([Setting, SectionTree, Article, Remark, Section])