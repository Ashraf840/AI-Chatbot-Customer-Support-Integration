# Generated by Django 4.2 on 2023-07-09 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_csovisitorconvoinfo_is_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='customersupportrequest',
            name='registered_user_email',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='User Email'),
        ),
    ]
