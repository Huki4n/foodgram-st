import base64
import imghdr

from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
  def to_internal_value(self, data):
    from django.core.files.uploadedfile import SimpleUploadedFile

    if isinstance(data, str) and data.startswith('data:image'):
      format, imgstr = data.split(';base64,')
      ext = format.split('/')[-1]
      filename = f"temp.{ext}"
      try:
        decoded_file = base64.b64decode(imgstr)
      except TypeError:
        raise serializers.ValidationError("Неверные данные изображения.")

      # Проверяем, действительно ли это изображение
      if imghdr.what(None, h=decoded_file) is None:
        raise serializers.ValidationError("Загруженный файл не является корректным файлом изображения.")

      data = SimpleUploadedFile(
        name=filename,
        content=decoded_file,
        content_type=f"image/{ext}"
      )
    return super().to_internal_value(data)
