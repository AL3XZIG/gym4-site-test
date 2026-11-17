import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="CampaignSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Выборы президента гимназии", max_length=180)),
                ("intro", models.TextField(blank=True)),
                ("rules", models.TextField(blank=True)),
                ("campaign_open", models.BooleanField(default=False)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("organizer", "Организатор"), ("moderator", "Модератор"), ("candidate", "Кандидат")], default="candidate", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Candidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_id", models.SlugField(max_length=80, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="candidate", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("public_id",)},
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(choices=[("profile", "Карточка кандидата"), ("material", "Агитационный материал"), ("news", "Новость кампании")], max_length=16)),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("pending", "На проверке"), ("published", "Опубликовано"), ("rejected", "Нужны исправления")], default="draft", max_length=16)),
                ("title", models.CharField(max_length=180)),
                ("summary", models.CharField(blank=True, max_length=500)),
                ("body", models.TextField(blank=True)),
                ("class_label", models.CharField(blank=True, max_length=40)),
                ("program", models.JSONField(blank=True, default=list)),
                ("category", models.CharField(choices=[("news", "Новости"), ("events", "Мероприятия"), ("announcements", "Объявления")], default="news", max_length=16)),
                ("attachment", models.FileField(blank=True, upload_to="submissions/%Y/%m/", validators=[django.core.validators.FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp", "pdf"])])),
                ("source_url", models.URLField(blank=True, max_length=500)),
                ("moderator_note", models.CharField(blank=True, max_length=1000)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="election_submissions", to=settings.AUTH_USER_MODEL)),
                ("candidate", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="submissions", to="elections.candidate")),
                ("reviewed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reviewed_submissions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="AuditEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=40)),
                ("details", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("submission", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="elections.submission")),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddIndex(
            model_name="submission",
            index=models.Index(fields=["status", "kind", "-published_at"], name="elections_s_status_7c2a4b_idx"),
        ),
        migrations.AddIndex(
            model_name="submission",
            index=models.Index(fields=["candidate", "status", "kind"], name="elections_s_candida_51aa2e_idx"),
        ),
    ]
