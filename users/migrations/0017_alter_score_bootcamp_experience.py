# Generated by Django 4.2.11 on 2024-06-16 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_score_courses_taken_alter_score_depart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='bootcamp_experience',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], null=True),
        ),
    ]