from urllib.parse import urlsplit
from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    program_text = forms.CharField(
        label="Пункты программы",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Один пункт программы на строку"}),
        help_text="Для карточки кандидата. До 8 пунктов.",
    )

    class Meta:
        model = Submission
        fields = ("kind", "title", "summary", "body", "class_label", "category", "source_url", "attachment")
        labels = {
            "kind": "Тип материала",
            "title": "Заголовок / имя кандидата",
            "summary": "Краткое описание / слоган",
            "body": "Основной текст",
            "class_label": "Класс (для карточки кандидата)",
            "category": "Категория новости",
            "source_url": "Ссылка на источник (необязательно)",
            "attachment": "Плакат или файл (JPG, PNG, WebP, PDF; до 8 МБ)",
        }
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 2}),
            "body": forms.Textarea(attrs={"rows": 7}),
        }

    def clean_program_text(self):
        raw = self.cleaned_data.get("program_text", "")
        items = [line.strip() for line in raw.splitlines() if line.strip()]
        if len(items) > 8:
            raise forms.ValidationError("Можно добавить не более 8 пунктов.")
        if any(len(item) > 240 for item in items):
            raise forms.ValidationError("Каждый пункт программы должен быть короче 240 символов.")
        return items

    def clean_body(self):
        value = self.cleaned_data.get("body", "")
        if len(value) > 5000:
            raise forms.ValidationError("Максимальный объём текста — 5 000 символов.")
        return value

    def clean_source_url(self):
        value = self.cleaned_data.get("source_url", "").strip()
        if value and urlsplit(value).scheme not in ("http", "https"):
            raise forms.ValidationError("Разрешены только HTTP(S)-ссылки.")
        return value

    def clean_attachment(self):
        uploaded = self.cleaned_data.get("attachment")
        if not uploaded:
            return uploaded
        if uploaded.size > 8 * 1024 * 1024:
            raise forms.ValidationError("Максимальный размер файла — 8 МБ.")
        extension = uploaded.name.rsplit(".", 1)[-1].lower() if "." in uploaded.name else ""
        header = uploaded.read(16)
        uploaded.seek(0)
        valid = (
            (extension in ("jpg", "jpeg") and header.startswith(b"\xff\xd8\xff"))
            or (extension == "png" and header.startswith(b"\x89PNG\r\n\x1a\n"))
            or (extension == "webp" and header.startswith(b"RIFF") and header[8:12] == b"WEBP")
            or (extension == "pdf" and header.startswith(b"%PDF-"))
        )
        if not valid:
            raise forms.ValidationError("Файл не прошёл проверку формата. Допустимы JPG, PNG, WebP и PDF.")
        return uploaded

    def clean(self):
        cleaned = super().clean()
        kind = cleaned.get("kind")
        if kind == Submission.Kind.PROFILE:
            uploaded = cleaned.get("attachment")
            if uploaded and uploaded.name.lower().endswith(".pdf"):
                self.add_error("attachment", "Для карточки кандидата можно загрузить только изображение.")
            if not cleaned.get("class_label"):
                self.add_error("class_label", "Укажите класс или параллель.")
            if not cleaned.get("body"):
                self.add_error("body", "Добавьте краткое представление кандидата.")
        if kind == Submission.Kind.MATERIAL and not cleaned.get("attachment") and not cleaned.get("source_url"):
            self.add_error("attachment", "Добавьте файл или ссылку на материал.")
        if kind == Submission.Kind.NEWS and not cleaned.get("summary"):
            self.add_error("summary", "Добавьте краткий анонс.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.program = self.cleaned_data.get("program_text", [])
        if commit:
            instance.save()
        return instance
