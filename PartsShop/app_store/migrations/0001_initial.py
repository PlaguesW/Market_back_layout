import app_store.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('register_date', models.DateTimeField(blank=True, null=True)),
                ('is_confirm', models.BooleanField(default=False)),
                ('wallet', models.PositiveBigIntegerField(default=0)),
                ('bank_number', models.PositiveBigIntegerField(validators=[app_store.models.bank_number_validate])),
                ('founder', models.OneToOneField(limit_choices_to={'is_seller': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StoreCheckout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_date', models.DateTimeField(blank=True, null=True)),
                ('bank_number', models.PositiveBigIntegerField(blank=True, null=True, validators=[app_store.models.bank_number_validate])),
                ('amount', models.PositiveBigIntegerField()),
                ('store', models.ForeignKey(limit_choices_to={'is_confirm': True}, on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to='app_store.store')),
            ],
        ),
    ]
