# Generated by Django 4.0 on 2021-12-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientId',
            fields=[
                ('national_id', models.CharField(editable=False, max_length=40, primary_key=True, serialize=False)),
            ],
        ),
    ]