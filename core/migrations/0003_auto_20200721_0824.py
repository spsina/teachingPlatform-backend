# Generated by Django 3.0.8 on 2020-07-21 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_quiz_quiz_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(related_name='classes', to='core.UserProfile'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teaching', to='core.UserProfile'),
        ),
    ]
