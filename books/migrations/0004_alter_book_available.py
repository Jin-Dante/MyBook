# Generated by Django 5.1.2 on 2024-11-11 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='available',
            field=models.CharField(choices=[('Private', 'Private'), ('Global', 'Global')], default='Private', max_length=8),
        ),
    ]
