from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


class ReadOnly(BasePermission):
  """Проверка на возможность редактирования"""

  def has_permission(self, request: Request, view: GenericViewSet) -> bool:
    return request.method in SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
  """Проверка на возможность редактирования только автором"""

  def has_permission(self, request: Request, view: GenericViewSet) -> bool:
    if request.method in SAFE_METHODS:
      return True

    return request.user and request.user.is_authenticated and request.user == view.get_object().author