# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('build_number', models.IntegerField()),
                ('build_name', models.CharField(max_length=200)),
                ('build_at', models.DateTimeField()),
            ],
            options={
                'ordering': ['build_name', 'build_number'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('glue', models.CharField(max_length=200)),
                ('build_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='cucumber_reports.BuildRun')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ScenarioDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('o', 'SCENARIO_OUTLINE'), ('s', 'SCENARIO'), ('b', 'BACKGROUND')], max_length=1)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenario_definitions', to='cucumber_reports.Feature')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ScenarioRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario_definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenario_runs', to='cucumber_reports.ScenarioDefinition')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StepDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('keyword', models.CharField(max_length=20)),
                ('scenario_definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_definitions', to='cucumber_reports.ScenarioDefinition')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StepRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.BigIntegerField()),
                ('status', models.CharField(choices=[('p', 'PASSED'), ('f', 'FAILED'), ('m', 'MISSING'), ('s', 'SKIPPED'), ('e', 'PENDING')], max_length=1)),
                ('error_msg', models.CharField(blank=True, max_length=200, null=True)),
                ('scenario_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_runs', to='cucumber_reports.ScenarioRun')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
