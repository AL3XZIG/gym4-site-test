from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.portal_login, name="portal-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="portal-logout"),
    path("", views.portal_home, name="portal-home"),
    path("submissions/new/", views.submission_create, name="submission-create"),
    path("submissions/<int:submission_id>/edit/", views.submission_edit, name="submission-edit"),
    path("submissions/<int:submission_id>/submit/", views.submission_submit, name="submission-submit"),
    path("moderation/", views.moderation_queue, name="moderation-queue"),
    path("moderation/<int:submission_id>/", views.submission_review, name="submission-review"),
]
