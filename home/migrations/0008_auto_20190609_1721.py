# Generated by Django 2.2.1 on 2019-06-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20190604_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orphan',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='m', help_text='Gender', max_length=1),
        ),
    ]
