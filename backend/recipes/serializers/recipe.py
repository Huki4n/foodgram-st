from functools import wraps
from typing import Optional, OrderedDict

from django.db.models import Model
from rest_framework import serializers
from rest_framework.request import Request

from api.serializers import Base64ImageField
from api.utils import many_unique_with_minimum_one_validate
from recipes.models.recipe import Recipe
from users.serializers import CommonUserSerializer
from .common_recipe import CommonActionRecipeSerializer, CommonRecipeSerializer
from .recipe_ingredients import RecipeIngredientsSerializer
from ..models.recipe_favorite import RecipeFavorite
from ..models.recipe_ingredients import RecipeIngredients
from ..models.shopping_cart import ShoppingCart


class RecipeSerializer(serializers.ModelSerializer):
  author = CommonUserSerializer()
  ingredients = RecipeIngredientsSerializer(
    many=True,
    source='recipe_ingredients',
  )
  text = serializers.CharField()

  class Meta:
    model = Recipe
    fields = (
      'id', 'name', 'text', 'image', 'cooking_time',
      'author', 'ingredients'
    )


class RecipeGetSerializer(RecipeSerializer):
  """Сериализатор получения рецептов"""

  is_favorite = serializers.SerializerMethodField()
  is_in_shopping_cart = serializers.SerializerMethodField()

  class Meta(RecipeSerializer.Meta):
    fields = (
      *RecipeSerializer.Meta.fields,
      'is_favorite', 'is_in_shopping_cart'
    )
    read_only_fields = fields

  def get_is_exists(self, obj: Recipe, model: Model):
    request: Optional[Request] = self.context.get('request')
    if not request or request.user.is_anonymous:
      return False
    return model.objects.filter(
      author=request.user, recipe=obj
    ).exists()

  def get_is_favorite(self, obj: Recipe):
    return self.get_is_exists(obj, RecipeFavorite)

  def get_is_in_shopping_cart(self, obj: Recipe):
    return self.get_is_exists(obj, ShoppingCart)


class RecipeUpdateSerializer(RecipeSerializer):
  """Сериализатор изменения рецептов"""

  author = CommonUserSerializer(default=serializers.CurrentUserDefault())
  ingredients = RecipeIngredientsSerializer(
    many=True,
    source='recipe_ingredients',
  )
  cooking_time = serializers.IntegerField(
    max_value=32767,
    min_value=1
  )
  image = Base64ImageField()

  class Meta(RecipeSerializer.Meta):
    read_only_fields = ('author',)
    fields = (
      'id', 'name', 'text', 'image', 'cooking_time',
      'author', 'ingredients'
    )

  def validate(self, data: OrderedDict):
    ingredients = data.get('recipe_ingredients')
    many_unique_with_minimum_one_validate(
      data_list=ingredients, field_name='ingredients',
      singular='ингредиент', plural='ингредиенты'
    )
    return data

  def added_ingredients(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
      validated_data = args[-1]
      ingredients = validated_data.pop('recipe_ingredients')

      recipe = func(self, *args, **kwargs)

      recipe.recipe_ingredients.all().delete()
      ingredient_recipe = [
        RecipeIngredients(
          recipe=recipe,
          ingredient=ingredient.get('id'),
          amount=ingredient.get('amount')
        ) for ingredient in ingredients
      ]
      RecipeIngredients.objects.bulk_create(ingredient_recipe)
      return recipe

    return wrapper

  @added_ingredients
  def create(self, validated_data: dict):
    return Recipe.objects.create(**validated_data)

  @added_ingredients
  def update(self, instance: Recipe, validated_data: dict):
    super().update(instance, validated_data)
    instance.recipe_ingredients.all().delete()
    return instance

  def to_representation(self, instance):
    return RecipeGetSerializer(instance, context=self.context).data
