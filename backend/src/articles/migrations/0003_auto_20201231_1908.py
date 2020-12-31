# Generated by Django 3.1.4 on 2020-12-31 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20200926_2118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-date_published',)},
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='link',
            field=models.URLField(max_length=512),
        ),
    ]