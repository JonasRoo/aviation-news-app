# Generated by Django 3.1.4 on 2021-01-05 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_auto_20210105_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.CharField(max_length=200)),
                ('is_abbreviation', models.BooleanField(default=False)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='tags.entity')),
            ],
        ),
    ]
