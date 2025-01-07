from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_product', '0002_alter_product_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sub', models.BooleanField(default=False)),
                ('body', models.TextField()),
                ('register_date', models.DateTimeField()),
                ('is_confirm', models.BooleanField(default=False)),
                ('product', models.ForeignKey(limit_choices_to={'is_confirm': True}, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_product.product')),
                ('sub_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcomments', to='app_comment.comment')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
