from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduleCollect",
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
                ("days", models.IntegerField()),
                ("scheduling", models.DateTimeField()),
                ("city", models.CharField(max_length=120)),
                (
                    "materials",
                    models.ManyToManyField(
                        related_name="schedule_collects", to="materials.material"
                    ),
                ),
            ],
        ),
    ]
