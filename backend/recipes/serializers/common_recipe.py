from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers import Base64ImageField
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from users.serializers import CommonUserSerializer


class CommonRecipeSerializer(serializers.ModelSerializer):
  """Базовый сериализатор рецептов."""

  image = Base64ImageField()

  class Meta:
    model = Recipe
    fields = ('id', 'name', 'image', 'cooking_time',)


class CommonActionRecipeSerializer(serializers.ModelSerializer):
  """Базовый сериализатор действий с рецептами"""

  author = CommonUserSerializer
  recipe = serializers.PrimaryKeyRelatedField(
    queryset=Recipe.objects.all()
  )

  class Meta:
    model = None
    fields = ('author', 'recipe')

  @classmethod
  def get_validators(cls):
    return [
      UniqueTogetherValidator(
        queryset=cls.Meta.model.objects.all(),
        fields=('author', 'recipe'),
      )
    ]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.Meta.validators = self.get_validators()

  def to_representation(self, instance):
    return CommonRecipeSerializer(instance.recipe).data