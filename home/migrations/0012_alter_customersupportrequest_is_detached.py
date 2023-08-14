# Generated by Django 4.2 on 2023-07-20 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_csovisitormessage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersupportrequest',
            name='is_detached',
            field=models.BooleanField(default=False, help_text="Mark as detached if the mark the 'CustomerSupportRequest' as resolved or dismissed", verbose_name='Detached'),
        ),
    ]
