# Generated by Django 4.2.5 on 2023-09-20 23:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_lesson_products"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessonviewing",
            name="date",
            field=models.DateField(auto_now=True),
        ),
    ]
