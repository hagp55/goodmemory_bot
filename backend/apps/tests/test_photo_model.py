from pathlib import Path

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.models import Photo

ALLOWED_PHOTO_FOR_UPLOAD = 10


@pytest.mark.django_db
def test_success_upload_photo(user) -> None:
    assert user.total_uploaded_photos == 0
    assert user.number_photos_available_for_upload == ALLOWED_PHOTO_FOR_UPLOAD
    number_photo = 3
    allowed_photo_for_upload = 10
    for _ in range(number_photo):
        photo: Photo = Photo(user=user, photo="test_photo.png")
        photo.full_clean()
        photo.save()

    assert user.total_uploaded_photos == number_photo
    assert user.number_photos_available_for_upload == allowed_photo_for_upload - number_photo


@pytest.mark.django_db
def test_not_success_upload_photo_after_limit(user) -> None:
    with pytest.raises(ValidationError, match="Ваш лимит исчерпан, попробуйте завтра"):
        number_photo = 11
        for _ in range(number_photo):
            photo: Photo = Photo(user=user, photo="test_photo.png")
            photo.full_clean()
            photo.save()

    assert user.total_uploaded_photos == ALLOWED_PHOTO_FOR_UPLOAD
    assert user.number_photos_available_for_upload == 0


@pytest.mark.django_db
def test_photo_delete_removes_file(user, test_media_root) -> None:
    test_image = SimpleUploadedFile(
        name="test_image.jpg", content=b"file_content", content_type="image/jpeg"
    )
    photo: Photo = Photo(user=user, photo=test_image)
    photo.full_clean()
    photo.save()

    file_path = Path(photo.photo.path)
    assert file_path.exists()

    photo.delete()
    assert not file_path.exists()
