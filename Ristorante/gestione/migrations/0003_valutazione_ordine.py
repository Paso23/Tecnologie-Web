# Generated by Django 4.2.16 on 2024-11-27 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordini', '0001_initial'),
        ('gestione', '0002_valutazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='valutazione',
            name='ordine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ordini.ordine'),
        ),
    ]
