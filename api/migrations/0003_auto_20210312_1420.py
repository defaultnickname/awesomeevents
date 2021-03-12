# Generated by Django 3.1.4 on 2021-03-12 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210312_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='code',
            field=models.CharField(default='CC91E9', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='thumbnail',
            field=models.ImageField(blank=True, default='thumbnail-default.jpg', upload_to=''),
        ),
    ]
