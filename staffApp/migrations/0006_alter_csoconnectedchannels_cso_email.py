# Generated by Django 4.2 on 2023-07-20 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffApp', '0005_alter_csoconnectedchannels_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csoconnectedchannels',
            name='cso_email',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='HDO active'),
        ),
    ]
