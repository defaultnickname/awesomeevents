# Generated by Django 3.1.4 on 2021-03-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='code',
            field=models.CharField(default='BC028C', max_length=8, unique=True),
        ),
    ]
