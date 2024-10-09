from typing import Literal

from django.contrib import admin
from django.utils.safestring import SafeText, mark_safe

from apps.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "uploaded_at",
        "get_preview_photo",
    )
    fields = (
        "user",
        "uploaded_at",
        "photo",
        "get_photo",
    )
    readonly_fields = (
        "get_photo",
        "uploaded_at",
    )

    @admin.display(description="Превью")
    def get_preview_photo(self, obj) -> SafeText | Literal["Фото отсутствует"]:
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="150px">')
        return "Фото отсутствует"

    @admin.display(description="Фото")
    def get_photo(self, obj) -> SafeText | Literal["Фото отсутствует"]:
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="800px">')
        return "Фото отсутствует"