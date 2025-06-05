from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator, MaxValueValidator, )
from django.db import models

from recipes.models.recipe import Recipe

User = get_user_model()


class RecipeFavorite(models.Model):
  """Модель избранных рецептов"""

  author = models.ForeignKey(
    to=User,
    verbose_name='Владелец избранного',
    on_delete=models.CASCADE,
  )
  recipe = models.ForeignKey(
    to=Recipe,
    verbose_name='Рецепт',
    on_delete=models.CASCADE,
  )

  class Meta:
    verbose_name = 'избранный рецепт'
    verbose_name_plural = 'Избранные рецепты'
    default_related_name = 'recipe_favorite'

    constraints = [
      models.UniqueConstraint(
        fields=('author', 'recipe'),
        name='unique_recipe_favorite'
      )
    ]

  def __str__(self) -> str:
      return f'Рецепт #{self.recipe.id}'
