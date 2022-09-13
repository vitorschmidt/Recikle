from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=120)),
                ("collect_days", models.PositiveIntegerField()),
                ("donation", models.BooleanField(default=False)),
                (
                    "materials",
                    models.ManyToManyField(
                        related_name="companies", to="materials.material"
                    ),
                ),
            ],
        ),
    ]
