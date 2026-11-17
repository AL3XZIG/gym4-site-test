import copy
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import AuditEvent, CampaignSettings, Candidate, Submission, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    max_num = 1

class GymUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super().get_fieldsets(request, obj))
        if not request.user.is_superuser:
            protected = {"is_staff", "is_superuser", "groups", "user_permissions"}
            for _, options in fieldsets:
                options["fields"] = tuple(
                    field for field in options["fields"] if field not in protected
                )
        return fieldsets

admin.site.unregister(User)
admin.site.register(User, GymUserAdmin)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("public_id", "user", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("public_id", "user__username", "user__first_name", "user__last_name")
    autocomplete_fields = ("user",)

@admin.register(CampaignSettings)
class CampaignSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not CampaignSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ("Информация о кампании", {"fields": ("title", "intro", "rules")}),
        ("Сроки", {"fields": ("campaign_open", "starts_at", "ends_at")}),
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "candidate", "author", "status", "created_at", "published_at")
    list_filter = ("kind", "status", "category")
    search_fields = ("title", "summary", "body", "author__username", "candidate__public_id")
    readonly_fields = ("author", "candidate", "kind", "status", "title", "summary", "body", "class_label", "program", "category", "attachment", "source_url", "moderator_note", "created_at", "updated_at", "submitted_at", "reviewed_by", "reviewed_at", "published_at")
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("action", "actor", "submission", "created_at")
    readonly_fields = ("actor", "submission", "action", "details", "created_at")
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
