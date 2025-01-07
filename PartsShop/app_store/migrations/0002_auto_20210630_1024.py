from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='quantity_of_products',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='store',
            name='sales_number',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
