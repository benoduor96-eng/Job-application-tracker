from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0002_interview"),
    ]

    operations = [
        migrations.CreateModel(
            name="CareerContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("company", models.CharField(blank=True, max_length=200)),
                ("contact_type", models.CharField(choices=[
                    ("recruiter", "Recruiter"), ("hiring_manager", "Hiring Manager"),
                    ("referral", "Referral"), ("interviewer", "Interviewer"),
                    ("career_coach", "Career Coach"), ("other", "Other")
                ], default="recruiter", max_length=30)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("profile_url", models.URLField(blank=True)),
                ("notes", models.TextField(blank=True)),
                ("last_contacted_at", models.DateTimeField(blank=True, null=True)),
                ("next_follow_up", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("application", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="contacts", to="jobs.jobapplication")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="career_contacts", to="auth.user")),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.AddIndex(
            model_name="careercontact",
            index=models.Index(fields=["user", "contact_type"], name="jobs_career_user_id_ctype"),
        ),
        migrations.AddIndex(
            model_name="careercontact",
            index=models.Index(fields=["user", "next_follow_up"], name="jobs_career_user_id_follow"),
        ),
    ]
