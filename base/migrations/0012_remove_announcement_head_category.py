# Generated by Django 4.1.4 on 2022-12-25 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_announcement_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='head_category',
        ),
    ]