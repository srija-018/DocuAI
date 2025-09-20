import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('Summarizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentmodel',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contentmodel',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
