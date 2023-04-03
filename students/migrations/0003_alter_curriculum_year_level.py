# Generated by Django 4.1.3 on 2023-04-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_curriculumsubject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='year_level',
            field=models.CharField(choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')], max_length=1),
        ),
    ]
