from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0003_rename_quantity_of_products_store_number_of_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='is_confirm',
        ),
        migrations.AlterField(
            model_name='storecheckout',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to='app_store.store'),
        ),
    ]
