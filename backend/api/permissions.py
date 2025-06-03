from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


class ReadOnly(BasePermission):
  """Проверка на возможность редактирование"""

  def has_permission(self, request: Request, view: GenericViewSet) -> bool:
    return request.method in SAFE_METHODS
