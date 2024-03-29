# Generated by Django 2.2.1 on 2019-06-28 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20190625_0517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adoptionrequest',
            options={'ordering': ['first_name', 'last_name', 'request_id']},
        ),
        migrations.AddField(
            model_name='donor',
            name='donation_remark',
            field=models.CharField(blank=True, help_text='Donation Remarks', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='donor',
            name='txnid',
            field=models.CharField(help_text='Transaction ID', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='orphanage',
            name='brief_desc',
            field=models.TextField(blank=True, help_text='Brief description of Orphanage', max_length=1024),
        ),
    ]
