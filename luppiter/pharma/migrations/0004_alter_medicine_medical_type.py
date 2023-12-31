# Generated by Django 4.2.2 on 2023-07-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharma", "0003_remove_order_medicine_order_medicine"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicine",
            name="medical_type",
            field=models.CharField(
                choices=[
                    ("painkiller", "PAINKILLERS"),
                    ("cardiovascular", "CARDIOVASCULAR"),
                ],
                max_length=100,
            ),
        ),
    ]
