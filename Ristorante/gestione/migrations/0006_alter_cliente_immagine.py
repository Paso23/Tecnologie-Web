# Generated by Django 4.2.16 on 2024-12-03 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0005_alter_cliente_immagine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='immagine',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
