# Generated by Django 5.1.4 on 2025-01-09 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0003_repeatword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repeatword',
            name='date',
            field=models.DateTimeField(),
        ),
    ]