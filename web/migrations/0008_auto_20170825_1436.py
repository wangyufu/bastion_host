# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-25 06:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.SmallIntegerField(choices=[(0, '批量命令'), (1, '文件分发')])),
                ('content', models.TextField(verbose_name='任务内容')),
                ('timeout', models.IntegerField(default=300)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('pid', models.PositiveIntegerField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField(verbose_name='任务结果')),
                ('status', models.SmallIntegerField(choices=[(0, '成功'), (1, '失败'), (2, '执行中'), (3, '超时')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bind_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.BindHostUser')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Task')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tasklog',
            unique_together=set([('task', 'bind_host')]),
        ),
    ]
