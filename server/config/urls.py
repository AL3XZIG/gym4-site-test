from django.contrib import admin
from django.urls import include, path
from elections import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("portal/", include("elections.urls")),
    path("api/v1/public/election/", views.public_election, name="public-election"),
    path("api/v1/public/news/", views.public_news, name="public-news"),
    path("media/submissions/<int:submission_id>/", views.public_media, name="public-media"),
]
