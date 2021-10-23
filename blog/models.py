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


class SectionTree(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='name', unique=True)
    Section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)
    describe = models.CharField(max_length=50, verbose_name='describe', null=True)
    image = models.ImageField('照片', upload_to='uploadimg/', blank=True, null=True)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=255, verbose_name='writer')
    time = models.CharField(max_length=1000, verbose_name='time')
    title = models.CharField(max_length=255, verbose_name='title')
    body = models.CharField(max_length=60000, verbose_name='body')
    parent = models.CharField(max_length=255, verbose_name='parent')


class Remark(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, verbose_name='email')
    writer = models.CharField(max_length=255, verbose_name='writer')
    time = models.CharField(max_length=1000, verbose_name='time')
    body = models.CharField(max_length=60000, verbose_name='body')
    parent = models.CharField(max_length=255, verbose_name='parent')

