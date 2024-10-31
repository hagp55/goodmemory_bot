from typing import Literal

from django.contrib import admin, messages
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import ngettext

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
    actions = ["delete_selected_objects"]

    @admin.action(
        permissions=["delete"],
        description="Удалить выбранные фотографии",
    )
    def delete_selected_objects(self, request, queryset) -> None:
        for obj in queryset:
            obj.delete()
        self.message_user(
            request,
            ngettext(
                "%d Фотография была успешно удалена.",
                "%d Фотографии были успешно удалены.",
                queryset.count(),
            )
            % queryset.count(),
            messages.SUCCESS,
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


admin.site.disable_action("delete_selected")
