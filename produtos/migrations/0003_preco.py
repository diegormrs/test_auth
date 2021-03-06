# Generated by Django 3.0.5 on 2020-06-01 01:51

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
        ('produtos', '0002_auto_20200601_0151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('datainicio', models.DateTimeField(auto_now=True)),
                ('datafim', models.DateTimeField(blank=True, null=True)),
                ('canalvenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.CanalVenda')),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Estabelecimento')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.Produto')),
            ],
            options={
                'verbose_name': 'Preço',
                'db_table': 'preco',
            },
        ),
    ]
