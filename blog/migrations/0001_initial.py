# Generated by Django 3.2.8 on 2021-10-22 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('writer', models.CharField(max_length=255, verbose_name='writer')),
                ('time', models.CharField(max_length=1000, verbose_name='time')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('body', models.CharField(max_length=60000, verbose_name='body')),
                ('parent', models.CharField(max_length=255, verbose_name='parent')),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255, verbose_name='email')),
                ('writer', models.CharField(max_length=255, verbose_name='writer')),
                ('time', models.CharField(max_length=1000, verbose_name='time')),
                ('body', models.CharField(max_length=60000, verbose_name='body')),
                ('parent', models.CharField(max_length=255, verbose_name='parent')),
            ],
        ),
        migrations.CreateModel(
            name='SectionTree',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='name')),
                ('parent', models.CharField(max_length=255, verbose_name='parent')),
                ('level', models.CharField(max_length=255, verbose_name='level')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='name')),
                ('data', models.CharField(max_length=1000, verbose_name='data')),
            ],
        ),
    ]
