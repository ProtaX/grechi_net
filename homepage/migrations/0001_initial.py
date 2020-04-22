# Generated by Django 3.0.4 on 2020-04-21 12:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorData',
            fields=[
                ('email', models.EmailField(help_text='Enter your email', max_length=254, primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('package_weight', models.IntegerField(default=1000, validators=[django.core.validators.MaxValueValidator(5000), django.core.validators.MinValueValidator(100)])),
                ('weight_per_meal', models.IntegerField(default=200, validators=[django.core.validators.MaxValueValidator(500), django.core.validators.MinValueValidator(100)])),
                ('hungry_people', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'ordering': ['date', 'email'],
            },
        ),
    ]
