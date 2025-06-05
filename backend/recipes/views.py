from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.permissions import IsAuthorOrReadOnly
from .filters import IngredientFilter, RecipeFilter
from .paginations import CustomPageNumberPagination
from .serializers.ingredient import IngredientSerializer
from .serializers.recipe import RecipeSerializer, RecipeUpdateSerializer
from .models.ingredient import Ingredient
from .models.recipe import Recipe


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
  """Вьюсет ингредиентов."""

  queryset = Ingredient.objects.all()
  serializer_class = IngredientSerializer
  permission_classes = [AllowAny]
  pagination_class = None
  filter_backends = [DjangoFilterBackend]
  filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
  """Вьюсет рецептов."""

  queryset = Recipe.objects.all()
  serializer_class = RecipeUpdateSerializer
  pagination_class = CustomPageNumberPagination
  permission_classes=[IsAuthorOrReadOnly]
  filter_backends = [DjangoFilterBackend]
  filterset_class = RecipeFilter
  ordering = ['-id']

  def get_permissions(self):
    if (
        self.action == 'download_shopping_cart'
        or self.request.method == 'POST'
    ):
      self.permission_classes = [IsAuthenticated]
    return super().get_permissions()

  def perform_create(self, serializer: Serializer):
    serializer.is_valid(raise_exception=True)
    serializer.save(author=self.request.user)

  def partial_update(self, request: Request, *args, **kwargs):
    instance: Recipe = self.get_object()
    data = request.data.copy()

    serializer: Serializer = self.get_serializer(
      instance, data=data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    super().perform_update(serializer)
    return Response(serializer.data)

