from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_ticket', '0002_alter_ticket_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmessage',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticketmessages', to='app_ticket.ticket'),
        ),
    ]
