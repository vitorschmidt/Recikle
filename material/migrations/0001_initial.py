# Generated by Django 4.1 on 2022-09-02 14:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("dangerousness", models.BooleanField(default=False)),
                ("category", models.CharField(max_length=120)),
                ("infos", models.CharField(max_length=500)),
                ("decomposition", models.PositiveIntegerField()),
            ],
        ),
    ]
