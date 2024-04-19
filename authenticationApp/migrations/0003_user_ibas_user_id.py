# Generated by Django 4.2 on 2024-04-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticationApp", "0002_alter_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ibas_user_id",
            field=models.CharField(
                blank=True,
                help_text="ibas_uid_[Id Num]",
                max_length=150,
                null=True,
                verbose_name="iBAS++ User Id",
            ),
        ),
    ]
