import json
import tempfile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import CampaignSettings, Candidate, Submission, UserProfile

User = get_user_model()

class ElectionPortalTests(TestCase):
    def make_candidate(self, username, public_id):
        user = User.objects.create_user(username=username, password="A-long-test-password-123")
        user.profile.role = UserProfile.Role.CANDIDATE
        user.profile.save()
        candidate = Candidate.objects.create(user=user, public_id=public_id)
        return user, candidate

    def make_profile(self, candidate, status=Submission.Status.PUBLISHED, title="Кандидат"):
        return Submission.objects.create(
            candidate=candidate,
            author=candidate.user,
            kind=Submission.Kind.PROFILE,
            status=status,
            title=title,
            summary="Предложения учеников",
            body="Краткое представление",
            class_label="10А",
            program=["Первое предложение"],
        )

    def test_public_api_contains_only_published_candidate_profiles(self):
        user, candidate = self.make_candidate("candidate-a", "candidate-a")
        self.make_profile(candidate, Submission.Status.DRAFT, "Черновик")
        response = self.client.get(reverse("public-election"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["mode"], "live")
        self.assertFalse(payload["demoOnly"])
        self.assertEqual(payload["candidates"], [])

        self.make_profile(candidate, Submission.Status.PUBLISHED, "Опубликованный кандидат")
        Submission.objects.create(
            candidate=candidate,
            author=user,
            kind=Submission.Kind.MATERIAL,
            status=Submission.Status.PUBLISHED,
            title="Программа в PDF",
            summary="Подробное описание материала",
            source_url="https://example.org/program.pdf",
        )
        response = self.client.get(reverse("public-election"))
        self.assertEqual(response.status_code, 200)
        public_candidate = response.json()["candidates"][0]
        self.assertEqual(public_candidate["name"], "Опубликованный кандидат")
        self.assertEqual(public_candidate["materials"][0]["description"], "Подробное описание материала")

    def test_candidate_cannot_edit_another_candidate_draft(self):
        user_a, candidate_a = self.make_candidate("candidate-a", "candidate-a")
        user_b, candidate_b = self.make_candidate("candidate-b", "candidate-b")
        other_draft = self.make_profile(candidate_b, Submission.Status.DRAFT)
        self.client.force_login(user_a)
        response = self.client.get(reverse("submission-edit", args=[other_draft.pk]))
        self.assertEqual(response.status_code, 404)

    def test_candidate_can_submit_own_draft_for_moderation(self):
        user, candidate = self.make_candidate("candidate-a", "candidate-a")
        draft = self.make_profile(candidate, Submission.Status.DRAFT)
        CampaignSettings.objects.create(campaign_open=True)
        self.client.force_login(user)
        response = self.client.post(reverse("submission-submit", args=[draft.pk]))
        self.assertEqual(response.status_code, 302)
        draft.refresh_from_db()
        self.assertEqual(draft.status, Submission.Status.PENDING)
        self.assertIsNotNone(draft.submitted_at)

    def test_organizer_role_grants_only_scoped_admin_access(self):
        organizer = User.objects.create_user(username="organizer", password="A-long-test-password-123")
        organizer.profile.role = UserProfile.Role.ORGANIZER
        organizer.profile.save()
        organizer.refresh_from_db()
        self.assertTrue(organizer.is_staff)
        self.assertTrue(organizer.has_perm("auth.add_user"))
        self.assertTrue(organizer.has_perm("elections.add_candidate"))
        self.assertFalse(organizer.is_superuser)
        self.assertFalse(organizer.has_perm("auth.delete_user"))

    def test_scoped_organizer_cannot_edit_superuser_flags(self):
        organizer = User.objects.create_user(username="organizer", password="A-long-test-password-123")
        organizer.profile.role = UserProfile.Role.ORGANIZER
        organizer.profile.save()
        target = User.objects.create_user(username="candidate-target", password="A-long-test-password-123")
        self.client.force_login(organizer)
        response = self.client.get(reverse("admin:auth_user_change", args=[target.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertNotIn('name="is_superuser"', html)
        self.assertNotIn('name="is_staff"', html)
        self.assertNotIn('name="user_permissions"', html)

    def test_candidate_cannot_open_moderation_queue(self):
        user, candidate = self.make_candidate("candidate-a", "candidate-a")
        self.client.force_login(user)
        response = self.client.get(reverse("moderation-queue"))
        self.assertEqual(response.status_code, 302)

    def test_closed_campaign_does_not_accept_submission(self):
        user, candidate = self.make_candidate("candidate-a", "candidate-a")
        draft = self.make_profile(candidate, Submission.Status.DRAFT)
        CampaignSettings.objects.create(campaign_open=False)
        self.client.force_login(user)
        response = self.client.post(reverse("submission-submit", args=[draft.pk]))
        self.assertEqual(response.status_code, 302)
        draft.refresh_from_db()
        self.assertEqual(draft.status, Submission.Status.DRAFT)

    def test_moderator_dashboard_does_not_show_private_drafts(self):
        moderator = User.objects.create_user(username="moderator", password="A-long-test-password-123")
        moderator.profile.role = UserProfile.Role.MODERATOR
        moderator.profile.save()
        candidate_user, candidate = self.make_candidate("candidate-a", "candidate-a")
        draft = self.make_profile(candidate, Submission.Status.DRAFT, "Private draft")
        pending = self.make_profile(candidate, Submission.Status.PENDING, "Pending profile")
        self.client.force_login(moderator)
        response = self.client.get(reverse("portal-home"))
        self.assertEqual(response.status_code, 200)
        visible = list(response.context["submissions"])
        self.assertNotIn(draft, visible)
        self.assertIn(pending, visible)

    def test_inactive_candidate_material_is_not_public(self):
        user, candidate = self.make_candidate("candidate-a", "candidate-a")
        profile = self.make_profile(candidate, Submission.Status.PUBLISHED)
        candidate.is_active = False
        candidate.save()
        response = self.client.get(reverse("public-election"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["candidates"], [])
        media_response = self.client.get(reverse("public-media", args=[profile.pk]))
        self.assertEqual(media_response.status_code, 404)

    def test_unpublished_upload_is_not_publicly_accessible(self):
        user, candidate = self.make_candidate("candidate-a", "candidate-a")
        with tempfile.TemporaryDirectory() as media_dir, override_settings(MEDIA_ROOT=media_dir):
            draft = Submission.objects.create(
                candidate=candidate,
                author=user,
                kind=Submission.Kind.MATERIAL,
                status=Submission.Status.DRAFT,
                title="Плакат",
                attachment=SimpleUploadedFile("poster.png", b"\x89PNG\r\n\x1a\nfake", content_type="image/png"),
            )
            response = self.client.get(reverse("public-media", args=[draft.pk]))
            self.assertEqual(response.status_code, 404)
            draft.status = Submission.Status.PUBLISHED
            draft.save()
            response = self.client.get(reverse("public-media", args=[draft.pk]))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["X-Content-Type-Options"], "nosniff")
