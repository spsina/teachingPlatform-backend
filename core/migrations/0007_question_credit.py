# Generated by Django 3.0.8 on 2020-07-21 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_answer_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='credit',
            field=models.IntegerField(default=0),
        ),
    ]
