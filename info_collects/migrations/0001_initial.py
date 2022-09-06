# Generated by Django 4.1 on 2022-09-05 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("materials", "0001_initial"),
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InfoCollect",
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
                ("localization", models.CharField(max_length=128)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="info_collect",
                        to="companies.company",
                    ),
                ),
                (
                    "materials",
                    models.ManyToManyField(
                        related_name="info_collects", to="materials.material"
                    ),
                ),
            ],
        ),
    ]
