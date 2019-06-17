# Generated by Django 2.2.1 on 2019-06-17 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20190615_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='adoptionrequest',
            name='approved',
            field=models.BooleanField(choices=[(True, 'Approved'), (False, 'Declined')], default=False),
        ),
        migrations.AddField(
            model_name='adoptionrequest',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='adoptionrequest',
            name='married',
            field=models.CharField(choices=[('m', 'Married'), ('u', 'Un-married'), ('d', 'Divorced')], default='m', help_text='Marriage Status', max_length=1),
        ),
    ]
