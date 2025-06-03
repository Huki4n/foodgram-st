from djoser.serializers import UserSerializer
from rest_framework import serializers

from api.serializers import Base64ImageField
from .models import User


class CurrentUserSerializer(UserSerializer):
  """Сериализатор текущего пользователя"""

  is_subscribed = serializers.BooleanField(default=False, read_only=True)

  class Meta:
    model = User
    fields = (
      'id',
      'email',
      'username',
      'first_name',
      'last_name',
      'avatar',
      'is_subscribed',
    )


class CommonUserSerializer(CurrentUserSerializer):
  """Общий сериализатор пользователя."""

  is_subscribed = serializers.SerializerMethodField()

  def get_is_subscribed(self, obj):
    request = self.context['request']
    user = request.user
    if user.is_anonymous:
      return False
    return obj.authors.filter(user=user).exists()


class AvatarSerializer(serializers.Serializer):
  """Сериализатор для обновления аватара"""

  avatar = Base64ImageField()

  def update(self, instance, validated_data):
    """Обновление аватара пользователя."""
    instance.avatar = validated_data.get('avatar', instance.avatar)
    instance.save()
    return instance
