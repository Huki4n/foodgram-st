from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django_filters import rest_framework as django_filters

from .models.ingredient import Ingredient
from .models.recipe import Recipe

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
  """Фильтр ингредиентов по названию"""

  name = django_filters.CharFilter(lookup_expr='startswith')

  class Meta:
    model = Ingredient
    fields = ['name']


class RecipeFilter(django_filters.FilterSet):
  """Фильтр ингредиентов по названию"""

  is_favorite = django_filters.BooleanFilter(
    field_name='is_favorite',
    method='filter_is_favorite'
  )
  is_in_shopping_cart = django_filters.BooleanFilter(
    field_name='is_in_shopping_cart',
    method='filter_is_in_shopping_cart'
  )
  author = django_filters.ModelChoiceFilter(queryset=User.objects.all())

  class Meta:
    model = Recipe
    fields = ['author']

  def filter_or_exclude_author(self, queryset: QuerySet, name: str, value: bool, filter_field: str) -> QuerySet:
    author = self.request.user
    if value and author.is_authenticated:
      return queryset.filter(**{filter_field: author}).distinct()
    elif not value and author.is_authenticated:
      return queryset.exclude(**{filter_field: author})
    elif not value and author.is_anonymous:
      return queryset.all()
    return queryset.none()

  def filter_is_favorite(
      self, queryset: QuerySet, name: str, value: bool
  ) -> QuerySet:
    return self.filter_or_exclude_author(
      queryset, name, value, filter_field='recipe_favorite__author'
    )

  def filter_is_in_shopping_cart(
      self, queryset: QuerySet, name: str, value: bool
  ) -> QuerySet:
    return self.filter_or_exclude_author(
      queryset, name, value, filter_field='shopping_cart__author'
    )
