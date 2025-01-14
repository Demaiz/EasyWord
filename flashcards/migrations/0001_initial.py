# Generated by Django 5.1.4 on 2024-12-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=20)),
                ('translation', models.CharField(max_length=35)),
                ('level', models.CharField(max_length=2)),
                ('audio_link', models.CharField(max_length=130)),
                ('phonetics', models.CharField(blank=True, max_length=25)),
                ('example', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]
