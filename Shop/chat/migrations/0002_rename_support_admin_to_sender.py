# Generated migration for chat app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Remove session_id field from supportsession
        migrations.RemoveField(
            model_name='supportsession',
            name='session_id',
        ),
        # Rename support_admin to sender and make it non-nullable
        migrations.RenameField(
            model_name='chatmessage',
            old_name='support_admin',
            new_name='sender',
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
