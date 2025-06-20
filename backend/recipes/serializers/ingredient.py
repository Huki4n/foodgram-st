from rest_framework import serializers

from recipes.models.ingredient import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
  """Сериализатор ингредиентов."""

  class Meta:
    model = Ingredient
    fields = ('id', 'name', 'measurement_unit',)