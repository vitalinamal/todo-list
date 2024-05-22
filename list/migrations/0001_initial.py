# Generated by Django 5.0.6 on 2024-05-22 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=40, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Task",
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
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("completed", models.BooleanField(default=False)),
                (
                    "tag",
                    models.ManyToManyField(
                        blank=True, null=True, related_name="tags", to="list.tag"
                    ),
                ),
            ],
            options={
                "ordering": ["completed", "-created_at"],
            },
        ),
    ]
