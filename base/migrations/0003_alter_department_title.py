# Generated by Django 4.1.4 on 2022-12-20 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_researchstatus_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]