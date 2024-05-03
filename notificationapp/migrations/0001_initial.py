# Generated by Django 4.2.11 on 2024-03-27 15:58

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
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nid', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('MONREQ', 'Money Request'), ('MONREC', 'Money Recieved'), ('TRANSUC', 'Transaction Success'), ('TRANPEN', 'Transaction Pending'), ('TRANDEC', 'Transaction Declined'), ('ACCVER', 'Account Verified'), ('ACCSUS', 'Account Suspended'), ('INFO', 'Information')], default='INFO', max_length=10)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('message', models.TextField(default='')),
                ('title', models.TextField(default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
