# Generated by Django 3.2.4 on 2025-01-08 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sub', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('register_date', models.DateTimeField()),
                ('sub_category', models.ForeignKey(blank=True, limit_choices_to={'is_sub': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='app_product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('sales_number', models.PositiveSmallIntegerField(default=0)),
                ('stock', models.PositiveSmallIntegerField(default=0)),
                ('is_confirm', models.BooleanField(default=False)),
                ('is_exists', models.BooleanField(default=False)),
                ('register_date', models.DateTimeField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_product.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_store.store')),
            ],
        ),
    ]
