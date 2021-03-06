# Generated by Django 3.2.8 on 2021-10-24 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_articlesystem_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='section',
            field=models.IntegerField(default=0, max_length=200, verbose_name='section'),
        ),
        migrations.AlterField(
            model_name='article',
            name='parent',
            field=models.IntegerField(default=0, max_length=200, verbose_name='parent'),
        ),
    ]
