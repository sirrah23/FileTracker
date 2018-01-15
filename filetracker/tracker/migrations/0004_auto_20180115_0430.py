# Generated by Django 2.0.1 on 2018-01-15 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_filehistory_inserted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileentity',
            name='status',
            field=models.CharField(blank=True, choices=[('n', 'Non-existent'), ('t', 'Tracked'), ('m', 'Modified')], default='n', help_text='Status of the file', max_length=1),
        ),
    ]
