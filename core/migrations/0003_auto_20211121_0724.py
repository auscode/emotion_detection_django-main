# Generated by Django 3.2.7 on 2021-11-21 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_emotion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('type', models.CharField(choices=[('happy', 'happy'), ('sad', 'sad'), ('fear', 'fear'), ('angry', 'angry'), ('disgust', 'disgust'), ('surprise', 'surprise'), ('neutral', 'neutral')], max_length=50)),
                ('link', models.CharField(max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='Music',
        ),
    ]
