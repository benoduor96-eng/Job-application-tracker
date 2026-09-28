from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('job_url', models.URLField(blank=True)),
                ('status', models.CharField(choices=[('saved', 'Saved'), ('applied', 'Applied'), ('screening', 'Screening'), ('interview', 'Interview'), ('offer', 'Offer'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='saved', max_length=20)),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('applied_date', models.DateField(blank=True, null=True)),
                ('next_action', models.CharField(blank=True, max_length=255)),
                ('next_action_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-updated_at']},
        ),
    ]