# Generated by Django 3.2.3 on 2021-05-17 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evox_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]