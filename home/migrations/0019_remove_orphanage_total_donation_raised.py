# Generated by Django 2.2.1 on 2019-06-29 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20190629_0449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orphanage',
            name='total_donation_raised',
        ),
    ]
