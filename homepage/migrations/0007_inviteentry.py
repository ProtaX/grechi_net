# Generated by Django 3.0.4 on 2020-05-04 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_auto_20200503_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteEntry',
            fields=[
                ('email', models.EmailField(help_text='Enter your email', max_length=254, primary_key=True, serialize=False)),
                ('invite_id', models.CharField(max_length=128, null=True, unique=True)),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
