# Generated by Django 4.2.3 on 2023-08-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='measurement_unit',
            field=models.CharField(choices=[('г', 'грамм'), ('кг', 'килограмм'), ('мл', 'миллилитр'), ('л', 'литр'), ('шт', 'штука'), ('ст.л.', 'столовая ложка'), ('по вкусу', 'по вкусу'), ('щепотка', 'щепотка')], max_length=100, verbose_name='Единицы измерения'),
        ),
    ]
