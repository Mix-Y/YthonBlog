# Generated by Django 3.2.8 on 2021-10-24 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_article_ftitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlesystem',
            name='section',
            field=models.IntegerField(max_length=200, verbose_name='level'),
        ),
    ]
