# Generated by Django 4.0.5 on 2022-07-15 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_attendancereport_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(default='media/avatar.svg', upload_to='media/profiles'),
        ),
    ]
