# Generated by Django 4.0.3 on 2022-03-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(default='True', max_length=255, verbose_name='Описание'),
        ),
    ]