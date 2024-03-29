# Generated by Django 2.2.1 on 2019-05-17 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20190516_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orphanage',
            name='brief_desc',
            field=models.TextField(blank=True, help_text='Brief description of Orphanage', max_length=512),
        ),
        migrations.AlterField(
            model_name='orphanage',
            name='total_donation_raised',
            field=models.FloatField(blank=True, help_text='Total donation raised through this website', null=True),
        ),
    ]
