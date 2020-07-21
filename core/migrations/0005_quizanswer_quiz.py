# Generated by Django 3.0.8 on 2020-07-21 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200721_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizanswer',
            name='quiz',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.Quiz'),
            preserve_default=False,
        ),
    ]
