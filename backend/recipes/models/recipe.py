from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator, MaxValueValidator, )
from django.db import models

from recipes.models.ingredient import Ingredient

User = get_user_model()


class Recipe(models.Model):
  """Модель рецепта"""

  author = models.ForeignKey(
    User,
    related_name='recipes',
    on_delete=models.CASCADE,
    verbose_name='Автор рецепта',
  )
  name = models.CharField(
    max_length=200,
    verbose_name='Название рецепта'
  )
  image = models.ImageField(
    verbose_name='Фотография рецепта',
    upload_to='recipes/',
    blank=True
  )
  text = models.TextField(
    verbose_name='Описание рецепта'
  )
  recipe_ingredients = models.ManyToManyField(
    Ingredient,
    through='RecipeIngredients',
    related_name='recipe_ingredients',
    verbose_name='Ингредиенты'
  )
  cooking_time = models.PositiveSmallIntegerField(
    'Время приготовления',
    validators=[
      MinValueValidator(1, message='Минимальное значение 1!'),
    ]
  )
  created = models.DateTimeField(
    auto_now_add=True,
    db_index=True,
    verbose_name='Дата публикации рецепта'
  )

  class Meta:
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'
    ordering = ('-created',)

  def __str__(self):
    return self.name