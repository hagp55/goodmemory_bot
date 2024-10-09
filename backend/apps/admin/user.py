from typing import Literal

from django.contrib import admin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    AdminUserCreationForm,
    UserChangeForm,
)
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import Photo, User


class PhotoInline(admin.TabularInline):
    model = Photo
    verbose_name_plural = "Фотографии"
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
class UserAdmin(admin.ModelAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "telegram_id",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "reference_date")},
        ),
        (
            _("Information about photos"),
            {
                "fields": (
                    "total_uploaded_photos",
                    "number_photos_available_for_upload",
                )
            },
        ),
    )
    inlines = (PhotoInline,)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = AdminUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "username",
        "email",
        "telegram_id",
        "is_staff",
    )
    readonly_fields = (
        "reference_date",
        "total_uploaded_photos",
        "number_photos_available_for_upload",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
