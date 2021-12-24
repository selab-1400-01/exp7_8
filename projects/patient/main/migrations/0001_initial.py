# Generated by Django 4.0 on 2021-12-23 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('national_id', models.CharField(db_index=True, editable=False, max_length=40, unique=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
