from rest_framework import serializers

from recipes.models.ingredient import Ingredient
from recipes.models.recipe_ingredients import RecipeIngredients


class RecipeIngredientsSerializer(serializers.ModelSerializer):
  id = serializers.PrimaryKeyRelatedField(
    queryset=Ingredient.objects.all(),
    source='ingredient',
    required=True
  )
  amount = serializers.IntegerField(
    min_value=1,
    max_value=32767,
    required=True
  )

  class Meta:
    model = RecipeIngredients
    fields = ['id', 'amount']

  def to_representation(self, instance):
    data = super().to_representation(instance)
    if instance and instance.ingredient:
      ingredient = instance.ingredient
      data.update({
        'name': ingredient.name,
        'measurement_unit': ingredient.measurement_unit,
      })
    return data
