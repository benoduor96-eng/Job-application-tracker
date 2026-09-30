from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0003_careercontact"),
    ]

    operations = [
        migrations.CreateModel(
            name="CareerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("headline", models.CharField(blank=True, max_length=200)),
                ("professional_summary", models.TextField(blank=True)),
                ("skills", models.JSONField(blank=True, default=list)),
                ("preferred_roles", models.JSONField(blank=True, default=list)),
                ("preferred_locations", models.JSONField(blank=True, default=list)),
                ("work_preference", models.CharField(
                    choices=[("remote", "Remote"), ("hybrid", "Hybrid"), ("onsite", "On-site"), ("flexible", "Flexible")],
                    default="flexible", max_length=20
                )),
                ("minimum_salary", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("target_salary", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("salary_currency", models.CharField(default="USD", max_length=3)),
                ("years_experience", models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ("portfolio_url", models.URLField(blank=True)),
                ("linkedin_url", models.URLField(blank=True)),
                ("github_url", models.URLField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="career_profile", to="auth.user")),
            ],
            options={"ordering": ["-updated_at"]},
        ),
    ]
