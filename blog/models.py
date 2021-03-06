from django.db import models
import os


# Create your models here.
class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='name', unique=True)
    data = models.CharField(max_length=1000, verbose_name='data')


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='name', unique=True)
    TreeSum = models.IntegerField(max_length=200, verbose_name='TreeSum', default=0)
    describe = models.CharField(max_length=50, verbose_name='describe', null=True)
    image = models.ImageField('照片', upload_to='uploadimg/', blank=True, null=True)
    parent = models.IntegerField(max_length=200, verbose_name='parent', default=0)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=255, verbose_name='writer')
    time = models.DateField(verbose_name='time', auto_now=True)
    title = models.CharField(max_length=255, verbose_name='title')
    ftitle = models.CharField(max_length=255, verbose_name='ftitle', default='null')
    body = models.CharField(max_length=60000, verbose_name='body')
    parent = models.IntegerField(max_length=200, verbose_name='parent', default=0)
    section = models.IntegerField(max_length=200, verbose_name='section', default=0)
    image = models.ImageField('照片', upload_to='uploadimg/', blank=True, null=True)


class Remark(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, verbose_name='email')
    writer = models.CharField(max_length=255, verbose_name='writer')
    time = models.DateField(verbose_name='time', auto_now=True)
    body = models.CharField(max_length=60000, verbose_name='body')
    parent = models.IntegerField(max_length=200, verbose_name='parent', default=0)


class ArticleSystem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='name')
    parent = models.IntegerField(max_length=200, verbose_name='parent', default=0)
    sum = models.IntegerField(max_length=200, verbose_name='sum', default=0)
    level = models.IntegerField(max_length=200, verbose_name='level', default=1)
    section = models.IntegerField(max_length=200, verbose_name='section')


class TimeMess(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=255, verbose_name='body')
    writer = models.CharField(max_length=255, verbose_name='writer')
    time = models.DateField(verbose_name='time', auto_now=True)
