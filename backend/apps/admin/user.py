from typing import Literal

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import Photo, User


class PhotoInline(admin.TabularInline):
    model = Photo
    verbose_name_plural = "Галерея"
    extra = 1
    fields = (
        "photo",
        "get_preview_photo",
    )
    readonly_fields = ("get_preview_photo",)

    @admin.display(description="Превью")
    def get_preview_photo(self, obj) -> SafeText | Literal["Фото отсутствует"]:
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="300px">')
        return "Фото отсутствует"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "telegram_id",
        "is_staff",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "telegram_id")},
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "reference_date")},
        ),
        (
            _("Information about photos"),
            {"fields": ("total_uploaded_photos", "number_photos_available_for_upload")},
        ),
    )
    readonly_fields = (
        # "reference_date",
        "total_uploaded_photos",
        "number_photos_available_for_upload",
    )

    inlines = (PhotoInline,)
