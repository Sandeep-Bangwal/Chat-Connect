# Generated by Django 4.2.4 on 2023-08-16 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0003_friendship_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_msg', models.TextField()),
                ('is_seen', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('sender_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senderBy', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]