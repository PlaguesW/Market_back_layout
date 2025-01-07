from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0004_auto_20210630_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='number_of_products',
        ),
        migrations.RemoveField(
            model_name='store',
            name='sales_number',
        ),
    ]
