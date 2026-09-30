from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("jobs", "0005_resume_careertask")]

    operations = [
        migrations.CreateModel(
            name="JobDescription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("company", models.CharField(max_length=200)),
                ("raw_text", models.TextField()),
                ("source_url", models.URLField(blank=True)),
                ("source", models.CharField(choices=[("company","Company"),("job_board","Job Board"),("referral","Referral"),("other","Other")], default="company", max_length=20)),
                ("required_skills", models.JSONField(blank=True, default=list)),
                ("preferred_skills", models.JSONField(blank=True, default=list)),
                ("responsibilities", models.JSONField(blank=True, default=list)),
                ("extracted_keywords", models.JSONField(blank=True, default=list)),
                ("salary_min", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("salary_max", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("analyzed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("application", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="job_description", to="jobs.jobapplication")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="job_descriptions", to="auth.user")),
            ],
            options={"ordering":["-updated_at"],"indexes":[
                models.Index(fields=["user","company"], name="jobs_jobdesc_user_id_1a2f_idx"),
                models.Index(fields=["user","-updated_at"], name="jobs_jobdesc_user_id_9e31_idx"),
            ]},
        ),
        migrations.CreateModel(
            name="ApplicationActivity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("activity_type", models.CharField(choices=[("created","Created"),("status_change","Status Change"),("note","Note"),("email","Email"),("call","Call"),("interview","Interview"),("follow_up","Follow Up"),("document","Document")], max_length=30)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("occurred_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("application", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="activities", to="jobs.jobapplication")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="application_activities", to="auth.user")),
            ],
            options={"ordering":["-occurred_at","-created_at"],"indexes":[
                models.Index(fields=["application","-occurred_at"], name="jobs_appact_applic_6b5d_idx"),
                models.Index(fields=["user","-occurred_at"], name="jobs_appact_user_id_9c11_idx"),
            ]},
        ),
        migrations.CreateModel(
            name="SavedSearch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("query", models.CharField(blank=True, max_length=200)),
                ("status", models.CharField(blank=True, max_length=20)),
                ("location", models.CharField(blank=True, max_length=200)),
                ("remote_only", models.BooleanField(default=False)),
                ("min_salary", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("max_salary", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("alerts_enabled", models.BooleanField(default=False)),
                ("last_used_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="saved_searches", to="auth.user")),
            ],
            options={"ordering":["-updated_at"]},
        ),
        migrations.AddConstraint(
            model_name="savedsearch",
            constraint=models.UniqueConstraint(fields=("user","name"), name="unique_saved_search_name"),
        ),
    ]
