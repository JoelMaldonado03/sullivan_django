# Generated by Django 4.2 on 2025-07-07 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0003_persona_cursos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='cursos',
        ),
    ]
