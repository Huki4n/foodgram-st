from rest_framework import serializers

from .common_recipe import CommonActionRecipeSerializer
from recipes.models.recipe_ingredients import RecipeIngredients
from recipes.models.shopping_cart import ShoppingCart


class ShoppingCartSerializer(CommonActionRecipeSerializer):
  """Сериализатор корзины"""

  class Meta(CommonActionRecipeSerializer.Meta):
    model = ShoppingCart
    error_message = 'Нельзя еще раз добавить рецепт в корзину'
