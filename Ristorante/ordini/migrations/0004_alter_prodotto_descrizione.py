# Generated by Django 4.2.16 on 2024-11-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordini', '0003_alter_prodotto_descrizione'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodotto',
            name='descrizione',
            field=models.CharField(blank=True, default='-', max_length=200, null=True),
        ),
    ]