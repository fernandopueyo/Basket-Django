# Generated by Django 4.2.6 on 2024-03-11 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendar_basket', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dorsal', models.BigIntegerField(null=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('id_team', models.ForeignKey(db_column='id_team', on_delete=django.db.models.deletion.CASCADE, to='calendar_basket.teams')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'players',
                'managed': True,
            },
        ),
    ]
