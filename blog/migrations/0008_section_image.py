# Generated by Django 3.2.8 on 2021-10-22 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_sectiontree_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='upload/', verbose_name='照片'),
        ),
    ]
