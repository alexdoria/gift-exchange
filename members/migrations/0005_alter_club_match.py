# Generated by Django 3.2.12 on 2022-05-18 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_club_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='match',
            field=models.JSONField(blank=True, default='dict'),
        ),
    ]
