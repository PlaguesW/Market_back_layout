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
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('T', 'technical'), ('F', 'financial'), ('O', 'orders'), ('E', 'etc')], max_length=50)),
                ('subject', models.CharField(max_length=200)),
                ('is_open', models.BooleanField(default=True)),
                ('last_update', models.DateTimeField()),
                ('open_date', models.DateTimeField()),
                ('close_date', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TicketMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('register_date', models.DateTimeField()),
                ('is_reply', models.BooleanField(default=False)),
                ('ticket', models.ForeignKey(limit_choices_to={'is_open': True}, on_delete=django.db.models.deletion.CASCADE, related_name='ticketmessages', to='app_ticket.ticket')),
            ],
        ),
    ]
