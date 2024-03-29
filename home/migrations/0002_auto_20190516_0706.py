# Generated by Django 2.2.1 on 2019-05-16 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adoptionrequest',
            old_name='num_family_mem',
            new_name='family_members',
        ),
        migrations.AlterField(
            model_name='adoptionrequest',
            name='income',
            field=models.FloatField(help_text='Annual income'),
        ),
        migrations.AlterField(
            model_name='adoptionrequest',
            name='phone_number',
            field=models.CharField(help_text='Phone number', max_length=32),
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(blank=True, help_text='Mobile number', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(help_text='Phone number', max_length=32),
        ),
        migrations.AlterField(
            model_name='donor',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Phone number', max_length=32, null=True),
        ),
    ]
