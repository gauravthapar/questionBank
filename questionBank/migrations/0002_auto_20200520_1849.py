# Generated by Django 3.0.6 on 2020-05-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionBank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='contact_no',
            field=models.CharField(blank=True, help_text='contact phone number', max_length=13),
        ),
    ]
