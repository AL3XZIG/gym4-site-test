import uuid
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

def submission_upload_path(instance, filename):
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
    return f"submissions/{uuid.uuid4().hex}.{suffix}"

class UserProfile(models.Model):
    class Role(models.TextChoices):
        ORGANIZER = "organizer", "Организатор"
        MODERATOR = "moderator", "Модератор"
        CANDIDATE = "candidate", "Кандидат"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CANDIDATE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, _ = Group.objects.get_or_create(name="Election organizers")
        if self.role == self.Role.ORGANIZER:
            allowed = (
                "add_user", "change_user", "view_user",
                "add_userprofile", "change_userprofile", "view_userprofile",
                "add_candidate", "change_candidate", "view_candidate",
                "add_campaignsettings", "change_campaignsettings", "view_campaignsettings",
                "view_submission", "view_auditevent",
            )
            permissions = Permission.objects.filter(
                content_type__app_label__in=("auth", "elections"),
                codename__in=allowed,
            )
            group.permissions.set(permissions)
            self.user.groups.add(group)
            if not self.user.is_staff:
                self.user.is_staff = True
                self.user.save(update_fields=("is_staff",))
        else:
            self.user.groups.remove(group)
            if self.user.is_staff and not self.user.is_superuser:
                self.user.is_staff = False
                self.user.save(update_fields=("is_staff",))

    def __str__(self):
        return f"{self.user.username}: {self.get_role_display()}"

class Candidate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="candidate")
    public_id = models.SlugField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("public_id",)

    def __str__(self):
        return self.public_id

class CampaignSettings(models.Model):
    title = models.CharField(max_length=180, default="Выборы президента гимназии")
    intro = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    campaign_open = models.BooleanField(default=False)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("CampaignSettings is a singleton and cannot be deleted.")

    def __str__(self):
        return self.title

class Submission(models.Model):
    class Kind(models.TextChoices):
        PROFILE = "profile", "Карточка кандидата"
        MATERIAL = "material", "Агитационный материал"
        NEWS = "news", "Новость кампании"

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PENDING = "pending", "На проверке"
        PUBLISHED = "published", "Опубликовано"
        REJECTED = "rejected", "Нужны исправления"

    class Category(models.TextChoices):
        NEWS = "news", "Новости"
        EVENTS = "events", "Мероприятия"
        ANNOUNCEMENTS = "announcements", "Объявления"

    candidate = models.ForeignKey(Candidate, null=True, blank=True, on_delete=models.PROTECT, related_name="submissions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="election_submissions")
    kind = models.CharField(max_length=16, choices=Kind.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    title = models.CharField(max_length=180)
    summary = models.CharField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    class_label = models.CharField(max_length=40, blank=True)
    program = models.JSONField(default=list, blank=True)
    category = models.CharField(max_length=16, choices=Category.choices, default=Category.NEWS)
    attachment = models.FileField(
        upload_to=submission_upload_path,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp", "pdf"])],
    )
    source_url = models.URLField(blank=True, max_length=500)
    moderator_note = models.CharField(max_length=1000, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_submissions")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("status", "kind", "-published_at"), name="elections_s_status_7c2a4b_idx"),
            models.Index(fields=("candidate", "status", "kind"), name="elections_s_candida_51aa2e_idx"),
        ]

    def __str__(self):
        return f"{self.get_kind_display()}: {self.title}"

class AuditEvent(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    submission = models.ForeignKey(Submission, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=40)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.action} · {self.created_at:%Y-%m-%d %H:%M}"
