from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
