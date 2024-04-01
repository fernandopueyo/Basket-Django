# Generated by Django 4.2.6 on 2024-03-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('num_jornada', models.BigIntegerField()),
                ('id_game', models.BigIntegerField(primary_key=True, serialize=False)),
                ('id_equipo_local', models.BigIntegerField()),
                ('id_equipo_visitante', models.BigIntegerField()),
                ('equipo_local', models.CharField(max_length=50)),
                ('equipo_visitante', models.CharField(max_length=50)),
                ('fecha_partido', models.DateField()),
                ('resultado_local', models.BigIntegerField(blank=True, null=True)),
                ('resultado_visitante', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'calendar',
                'ordering': ['num_jornada'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigIntegerField()),
                ('name', models.TextField()),
                ('id_team', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'teams',
                'managed': True,
            },
        ),
    ]