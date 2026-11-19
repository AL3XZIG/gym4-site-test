from copy import deepcopy
from html import escape

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import AuditEvent, Candidate, CampaignSettings, ElectionControlState, Submission


def _owner_check(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(_owner_check)
def control_center(request):
    state = ElectionControlState.load()
    candidates = Candidate.objects.filter(is_active=True, user__is_active=True).select_related("user")
    candidate_rows = []
    for candidate in candidates:
        profile = Submission.objects.filter(
            candidate=candidate, kind=Submission.Kind.PROFILE,
            status=Submission.Status.PUBLISHED,
        ).order_by("-published_at").first()
        candidate_rows.append({
            "id": candidate.pk,
            "public_id": candidate.public_id,
            "name": profile.title if profile else candidate.public_id,
            "votes": int(state.data.get("votes", {}).get(str(candidate.pk), 0)),
            "percent": state.data.get("manual_percentages", {}).get(str(candidate.pk)),
        })
    total = sum(item["votes"] for item in candidate_rows)
    for item in candidate_rows:
        item["calculated_percent"] = round(item["votes"] * 100 / total, 1) if total else 0
    events = AuditEvent.objects.filter(action__startswith="control_").select_related("actor")[:30]
    return render(request, "portal/control_center.html", {
        "state": state, "candidates": candidate_rows, "total": total,
        "events": events, "campaign": CampaignSettings.objects.first(),
    })


@login_required
@user_passes_test(_owner_check)
@require_POST
@transaction.atomic
def control_action(request):
    state = ElectionControlState.load(lock=True)
    action = request.POST.get("action", "")
    reason = request.POST.get("reason", "").strip()[:500]
    data = deepcopy(state.data or {})
    data.setdefault("votes", {})
    data.setdefault("manual_percentages", {})

    if action == "save_votes":
        candidate_id = request.POST.get("candidate_id", "")
        try:
            candidate = Candidate.objects.select_for_update().get(pk=int(candidate_id), is_active=True)
            votes = int(request.POST.get("votes", "-1"))
        except (ValueError, Candidate.DoesNotExist):
            messages.error(request, "Не удалось определить кандидата.")
            return redirect("election-control")
        if votes < 0 or votes > 1000000:
            messages.error(request, "Количество голосов должно быть от 0 до 1 000 000.")
            return redirect("election-control")
        if data.get("mode", "live") == "live" and not reason:
            messages.error(request, "Для исправления фактического подсчёта укажите причину.")
            return redirect("election-control")
        before = int(data["votes"].get(str(candidate.pk), 0))
        data["votes"][str(candidate.pk)] = votes
        event_details = {"candidate": candidate.public_id, "before": before, "after": votes, "reason": reason}
        event_action = "control_votes_corrected" if data.get("mode", "live") == "live" else "control_demo_votes_changed"
    elif action == "set_mode":
        mode = request.POST.get("mode")
        if mode not in ("live", "simulation"):
            messages.error(request, "Неизвестный режим.")
            return redirect("election-control")
        data["mode"] = mode
        event_action, event_details = "control_mode_changed", {"mode": mode}
    elif action == "save_percentages":
        if data.get("mode") != "simulation":
            messages.error(request, "Ручные проценты доступны только в режиме симуляции.")
            return redirect("election-control")
        for candidate in Candidate.objects.filter(is_active=True):
            raw = request.POST.get(f"percent_{candidate.pk}", "").strip()
            if raw:
                try:
                    value = float(raw.replace(",", "."))
                except ValueError:
                    messages.error(request, "Проверьте формат процентов.")
                    return redirect("election-control")
                if not 0 <= value <= 100:
                    messages.error(request, "Процент должен находиться в диапазоне 0–100.")
                    return redirect("election-control")
                data["manual_percentages"][str(candidate.pk)] = value
        event_action, event_details = "control_demo_percentages_changed", {"percentages": data["manual_percentages"]}
    elif action == "publish":
        state.published = True
        state.published_at = timezone.now()
        event_action, event_details = "control_results_published", {"mode": data.get("mode", "live")}
        campaign = CampaignSettings.objects.first()
        title = "Предварительные результаты выборов" if data.get("mode") == "live" else "Демонстрационные результаты выборов"
        rows = []
        total_votes = sum(int(value) for value in data["votes"].values())
        for candidate in Candidate.objects.filter(is_active=True, user__is_active=True):
            profile = Submission.objects.filter(candidate=candidate, kind=Submission.Kind.PROFILE, status=Submission.Status.PUBLISHED).order_by("-published_at").first()
            name = profile.title if profile else candidate.public_id
            votes = int(data["votes"].get(str(candidate.pk), 0))
            percent = data["manual_percentages"].get(str(candidate.pk)) if data.get("mode") == "simulation" else (round(votes * 100 / total_votes, 1) if total_votes else 0)
            rows.append(f"<li>{escape(name)}: {votes} голосов ({percent}%)</li>")
        body = "<p>Опубликовано из панели управления выборами.</p><ol>" + "".join(rows) + "</ol>"
        Submission.objects.create(
            author=request.user, kind=Submission.Kind.NEWS,
            status=Submission.Status.PUBLISHED, title=title,
            summary="Промежуточная статистика голосования.",
            body=body, category=Submission.Category.NEWS,
            published_at=timezone.now(),
        )
        if campaign:
            AuditEvent.objects.create(actor=request.user, action="control_news_created", details={"title": title})
    elif action == "unpublish":
        state.published = False
        event_action, event_details = "control_results_unpublished", {"reason": reason}
    else:
        messages.error(request, "Неизвестная операция.")
        return redirect("election-control")

    state.data = data
    state.updated_by = request.user
    state.save()
    AuditEvent.objects.create(actor=request.user, action=event_action, details=event_details)
    messages.success(request, "Изменения сохранены.")
    return redirect("election-control")


@login_required
@user_passes_test(_owner_check)
def control_health(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        database = "ok"
    except Exception:
        database = "error"
    state = ElectionControlState.load()
    return JsonResponse({
        "status": "ok" if database == "ok" else "degraded",
        "database": database,
        "mode": state.data.get("mode", "live"),
        "published": state.published,
        "checked_at": timezone.now().isoformat(),
    })
