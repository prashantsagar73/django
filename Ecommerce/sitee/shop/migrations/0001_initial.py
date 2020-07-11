# Generated by Django 3.0.6 on 2020-05-24 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('desc', models.CharField(max_length=400)),
                ('pub_date', models.DateField()),
            ],
        ),
    ]
