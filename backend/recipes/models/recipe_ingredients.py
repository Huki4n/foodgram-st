from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator, MaxValueValidator, )
from django.db import models

from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe

User = get_user_model()


class RecipeIngredientsQuerySet(models.QuerySet):
  """QuerySet для модели связи рецептов и ингредиентов."""

  def get_sum_amount(self):
    return self.annotate(total_amount=models.Sum('amount'))

  def order_by_ingredient_name(self):
    return self.order_by('ingredient__name')

  def rename_fields(self):
    return self.values(
      name=models.F('ingredient__name'),
      measurement_unit=models.F('ingredient__measurement_unit')
    )


class ShopCartManager(models.Manager):
  def get_queryset(self, author: User) -> RecipeIngredientsQuerySet:
    return (
      RecipeIngredientsQuerySet(self.model)
      .filter(recipe__shopping_cart__author=author)
      .rename_fields()
      .get_sum_amount()
      .order_by_ingredient_name()
    )


class RecipeIngredients(models.Model):
  """Модель ингредиентов в рецепте"""

  recipe = models.ForeignKey(
    Recipe,
    on_delete=models.CASCADE,
    related_name='ingredient_list',
    verbose_name='Рецепт',
  )
  ingredient = models.ForeignKey(
    Ingredient,
    on_delete=models.CASCADE,
    verbose_name='Ингредиент',
    related_name='in_recipe'
  )
  amount = models.PositiveSmallIntegerField(
    verbose_name='Количество',
    validators=[
      MinValueValidator(1, message='Минимальное количество 1!'),
      MaxValueValidator(32767, message='Максимальное количество 32767!'),
    ]
  )

  objects = RecipeIngredientsQuerySet.as_manager()
  shopping_list = ShopCartManager()

  class Meta:
    verbose_name = 'Ингредиент в рецепте'
    verbose_name_plural = 'Ингредиенты в рецептах'
    constraints = [
      models.UniqueConstraint(
        fields=('recipe', 'ingredient'),
        name='unique_recipe_ingredients'
      )
    ]

  def __str__(self):
    return f'{self.ingredient} {self.recipe}'