import mimetypes
from functools import wraps
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .forms import SubmissionForm
from .models import AuditEvent, CampaignSettings, Candidate, Submission, UserProfile

def current_role(user):
    if user.is_superuser:
        return UserProfile.Role.ORGANIZER
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile.role

def roles_required(*roles):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if current_role(request.user) not in roles:
                messages.error(request, "У вашей учётной записи нет доступа к этому разделу.")
                return redirect("portal-home")
            return view(request, *args, **kwargs)
        return wrapped
    return decorator

def portal_login(request):
    if request.user.is_authenticated:
        return redirect("portal-home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        redirect_to = request.POST.get("next") or request.GET.get("next", "")
        if not url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            redirect_to = "portal-home"
        return redirect(redirect_to)
    return render(request, "portal/login.html", {"form": form})

@login_required
def portal_home(request):
    role = current_role(request.user)
    candidate = None
    if role == UserProfile.Role.CANDIDATE:
        candidate = Candidate.objects.filter(user=request.user, is_active=True).first()
        submissions = Submission.objects.filter(author=request.user)
        if candidate is None:
            submissions = submissions.none()
    else:
        submissions = Submission.objects.all()
    queue = Submission.objects.filter(status=Submission.Status.PENDING) if role in (UserProfile.Role.ORGANIZER, UserProfile.Role.MODERATOR) else Submission.objects.none()
    return render(request, "portal/dashboard.html", {
        "role": role,
        "candidate": candidate,
        "submissions": submissions[:50],
        "queue": queue[:50],
    })

@roles_required(UserProfile.Role.CANDIDATE)
def submission_create(request):
    candidate = Candidate.objects.filter(user=request.user, is_active=True).first()
    if not candidate:
        messages.error(request, "Организатор ещё не привязал вашу учётную запись к карточке кандидата.")
        return redirect("portal-home")
    form = SubmissionForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        submission = form.save(commit=False)
        submission.author = request.user
        submission.candidate = candidate
        submission.status = Submission.Status.DRAFT
        submission.save()
        AuditEvent.objects.create(actor=request.user, submission=submission, action="draft_created")
        messages.success(request, "Черновик сохранён. Проверьте его и отправьте на модерацию.")
        return redirect("portal-home")
    return render(request, "portal/submission_form.html", {"form": form, "heading": "Новый материал"})

@roles_required(UserProfile.Role.CANDIDATE)
def submission_edit(request, submission_id):
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        author=request.user,
        status__in=(Submission.Status.DRAFT, Submission.Status.REJECTED),
    )
    form = SubmissionForm(request.POST or None, request.FILES or None, instance=submission, initial={
        "program_text": "\n".join(submission.program or []),
    })
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        updated.status = Submission.Status.DRAFT
        updated.moderator_note = ""
        updated.reviewed_by = None
        updated.reviewed_at = None
        updated.submitted_at = None
        updated.published_at = None
        updated.save()
        AuditEvent.objects.create(actor=request.user, submission=updated, action="draft_updated")
        messages.success(request, "Черновик обновлён.")
        return redirect("portal-home")
    return render(request, "portal/submission_form.html", {"form": form, "heading": "Изменить черновик"})

@roles_required(UserProfile.Role.CANDIDATE)
@require_POST
def submission_submit(request, submission_id):
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        author=request.user,
        status__in=(Submission.Status.DRAFT, Submission.Status.REJECTED),
    )
    submission.status = Submission.Status.PENDING
    submission.submitted_at = timezone.now()
    submission.moderator_note = ""
    submission.save(update_fields=("status", "submitted_at", "moderator_note", "updated_at"))
    AuditEvent.objects.create(actor=request.user, submission=submission, action="submitted_for_review")
    messages.success(request, "Материал отправлен организаторам на проверку.")
    return redirect("portal-home")

@roles_required(UserProfile.Role.ORGANIZER, UserProfile.Role.MODERATOR)
def moderation_queue(request):
    queue = Submission.objects.filter(status=Submission.Status.PENDING).select_related("author", "candidate")
    return render(request, "portal/moderation.html", {"queue": queue})

@roles_required(UserProfile.Role.ORGANIZER, UserProfile.Role.MODERATOR)
def submission_review(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, status=Submission.Status.PENDING)
    if request.method == "POST":
        action = request.POST.get("action")
        note = request.POST.get("moderator_note", "").strip()[:1000]
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.moderator_note = note
        if action == "approve":
            submission.status = Submission.Status.PUBLISHED
            submission.published_at = timezone.now()
            event = "approved_and_published"
        elif action == "reject":
            submission.status = Submission.Status.REJECTED
            submission.published_at = None
            event = "returned_for_changes"
        else:
            messages.error(request, "Неизвестное действие.")
            return redirect("submission-review", submission_id=submission.pk)
        submission.save()
        AuditEvent.objects.create(actor=request.user, submission=submission, action=event, details={"note": note})
        messages.success(request, "Решение сохранено.")
        return redirect("moderation-queue")
    return render(request, "portal/review.html", {"submission": submission})

def _campaign():
    return CampaignSettings.objects.first() or CampaignSettings.objects.create()

def _candidate_payload(candidate):
    profile = Submission.objects.filter(
        candidate=candidate, kind=Submission.Kind.PROFILE, status=Submission.Status.PUBLISHED
    ).order_by("-published_at").first()
    if not profile:
        return None
    materials = Submission.objects.filter(
        candidate=candidate, kind=Submission.Kind.MATERIAL, status=Submission.Status.PUBLISHED
    ).order_by("-published_at")[:12]
    return {
        "id": candidate.public_id,
        "name": profile.title,
        "class": profile.class_label,
        "slogan": profile.summary,
        "bio": profile.body,
        "program": profile.program or [],
        "poster": f"/media/submissions/{profile.pk}/" if profile.attachment else "",
        "materials": [
            {"title": item.title, "url": f"/media/submissions/{item.pk}/" if item.attachment else item.source_url}
            for item in materials
        ],
    }

def public_election(request):
    campaign = _campaign()
    candidates = []
    for candidate in Candidate.objects.filter(is_active=True, user__is_active=True).select_related("user"):
        payload = _candidate_payload(candidate)
        if payload:
            candidates.append(payload)
    return JsonResponse({
        "mode": "live",
        "demoOnly": False,
        "votingEnabled": False,
        "campaign": {
            "title": campaign.title,
            "intro": campaign.intro,
            "rules": campaign.rules,
            "campaignOpen": campaign.campaign_open,
            "startsAt": campaign.starts_at.isoformat() if campaign.starts_at else None,
            "endsAt": campaign.ends_at.isoformat() if campaign.ends_at else None,
        },
        "candidates": candidates,
    })

def public_news(request):
    posts = Submission.objects.filter(
        kind=Submission.Kind.NEWS, status=Submission.Status.PUBLISHED
    ).select_related("author", "candidate").order_by("-published_at")[:100]
    data = []
    for item in posts:
        data.append({
            "id": item.pk,
            "title": item.title,
            "date": (item.published_at or item.created_at).date().isoformat(),
            "category": item.category,
            "sourceName": "Кампания выборов",
            "sourceUrl": item.source_url,
            "excerpt": item.summary,
            "body": item.body,
            "imageUrl": f"/media/submissions/{item.pk}/" if item.attachment and item.attachment.name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) else "",
        })
    return JsonResponse({"posts": data})

def public_media(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, status=Submission.Status.PUBLISHED)
    if not submission.attachment:
        raise Http404
    name = submission.attachment.name.lower()
    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    is_image = content_type in ("image/jpeg", "image/png", "image/webp")
    response = FileResponse(
        submission.attachment.open("rb"),
        content_type=content_type,
        as_attachment=not is_image,
        filename="material" + (".pdf" if content_type == "application/pdf" else ".bin"),
    )
    response["X-Content-Type-Options"] = "nosniff"
    response["Content-Security-Policy"] = "default-src 'none'; sandbox"
    response["Cache-Control"] = "public, max-age=300"
    return response
