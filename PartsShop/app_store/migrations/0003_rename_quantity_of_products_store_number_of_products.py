from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0002_auto_20210630_1024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='quantity_of_products',
            new_name='number_of_products',
        ),
    ]
