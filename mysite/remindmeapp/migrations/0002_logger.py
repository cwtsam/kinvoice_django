# Generated by Django 3.0.5 on 2020-08-20 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remindmeapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=60)),
                ('item', models.CharField(max_length=60)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
