# Generated by Django 2.0.5 on 2019-09-04 05:32

import courses.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190903_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='order',
            field=courses.fields.OrderField(blank=True),
        ),
    ]
