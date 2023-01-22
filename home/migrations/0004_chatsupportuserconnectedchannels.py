# Generated by Django 4.1 on 2023-01-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_chatsupportuseronline"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatSupportUserConnectedChannels",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cso_email", models.CharField(blank=True, max_length=60, null=True)),
                (
                    "visitor_session_uuid",
                    models.CharField(blank=True, max_length=36, null=True),
                ),
                ("room_slug", models.CharField(max_length=25)),
                ("channel_value", models.CharField(max_length=74)),
            ],
            options={
                "verbose_name_plural": "Customer Support (Chat) CSO-Visitor Channels",
            },
        ),
    ]
