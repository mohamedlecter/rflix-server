# Generated by Django 5.1.4 on 2025-01-05 20:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_rating_personal_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('members', models.ManyToManyField(blank=True, related_name='movie_parties', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]