# Generated by Django 2.1.7 on 2019-06-26 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20190625_2219'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='skill',
            unique_together=set(),
        ),
    ]
