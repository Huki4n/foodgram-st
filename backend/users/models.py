from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USER_AVATAR_PATH = 'users/'


class User(AbstractUser):
  """Модель юзера"""

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  email = models.EmailField(
    verbose_name='Электронная почта',
    unique=True
  )
  username = models.CharField(
    max_length=150,
    verbose_name='Имя пользователя',
    unique=True,
    db_index=True,
    validators=[UnicodeUsernameValidator()]
  )
  first_name = models.CharField(
    max_length=150,
    verbose_name='Имя'
  )
  last_name = models.CharField(
    max_length=150,
    verbose_name='Фамилия'
  )
  avatar = models.ImageField(
    verbose_name='Аватар',
    blank=True,
    upload_to=USER_AVATAR_PATH
  )

  class Meta:
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'
    ordering = ('id',)

  def __str__(self):
    return self.username


class Subscription(models.Model):
  """Модель подписчиков"""

  author_recipe = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='authors',
    verbose_name='Автор рецепта'
  )
  user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='users',
    verbose_name='Подписчик'
  )
  created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Дата подписки'
  )

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=('author_recipe', 'user'),
        name='unique_author_recipe_user'
      )
    ]
    verbose_name = 'подписку'
    verbose_name_plural = 'Подписки'

  def __str__(self):
    return (
      f'{self.user.__str__()} {self.author_recipe.__str__()}'
    )