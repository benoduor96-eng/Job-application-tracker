from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0004_careerprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("summary", models.TextField(blank=True)),
                ("content", models.TextField(blank=True)),
                ("version", models.PositiveIntegerField(default=1)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("active", "Active"), ("archived", "Archived")], default="draft", max_length=20)),
                ("target_role", models.CharField(blank=True, max_length=200)),
                ("skills", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("source_application", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="resume_versions", to="jobs.jobapplication")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resumes", to="auth.user")),
            ],
            options={
                "ordering": ["-updated_at"],
                "indexes": [
                    models.Index(fields=["user", "status"], name="jobs_resume_user_id_7c2b75_idx"),
                    models.Index(fields=["user", "-updated_at"], name="jobs_resume_user_id_1b0b16_idx"),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="resume",
            constraint=models.UniqueConstraint(fields=("user", "name", "version"), name="unique_resume_version"),
        ),
        migrations.CreateModel(
            name="CareerTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("priority", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("urgent", "Urgent")], default="medium", max_length=20)),
                ("status", models.CharField(choices=[("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done"), ("cancelled", "Cancelled")], default="todo", max_length=20)),
                ("due_date", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("application", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="career_tasks", to="jobs.jobapplication")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="career_tasks", to="auth.user")),
            ],
            options={
                "ordering": ["status", "due_date", "-updated_at"],
                "indexes": [
                    models.Index(fields=["user", "status"], name="jobs_career_user_id_8cb0e8_idx"),
                    models.Index(fields=["user", "due_date"], name="jobs_career_user_id_1f0d5c_idx"),
                    models.Index(fields=["application", "status"], name="jobs_career_applica_4d6f57_idx"),
                ],
            },
        ),
    ]
