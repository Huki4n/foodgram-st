from djoser import views as djoser_views
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from api.permissions import ReadOnly
from .models import User
from .serializers import CommonUserSerializer, CurrentUserSerializer, AvatarSerializer


import logging
logger = logging.getLogger(__name__)


# Create your views here.
class CustomUserViewSet(djoser_views.UserViewSet):
  """ViewSet для работы с пользователями."""

  queryset = User.objects.all()
  serializer_class = CommonUserSerializer
  pagination_class = PageNumberPagination
  pagination_class.page_size_query_param = 'limit'
  permission_classes = [IsAuthenticated | ReadOnly]

  @action(
    methods=['get', 'put', 'patch', 'delete'],
    detail=False,
    url_path='me',
    url_name='me',
  )
  def me(self, request: Request):
    """Получение информации о текущем пользователе"""

    if not request.user.is_authenticated:
      raise NotAuthenticated("Authentication required.")

    serializer = self.get_serializer(instance=request.user)
    return Response(serializer.data)

  @action(
    methods=['put', 'delete'],
    detail=False,
    url_path='me/avatar',
    url_name='avatar',
    permission_classes=[IsAuthenticated],
  )
  def avatar(self, request: Request):
    """Обновление аватара текущего пользователя."""

    user = request.user

    if request.method == 'DELETE':
      user.avatar.delete(save=True)
      return response.Response(
        {'avatar': None},
        status=status.HTTP_204_NO_CONTENT
      )

    if 'avatar' not in request.data:
      return response.Response(
        {'avatar': 'Отсутствует изображение'},
        status=status.HTTP_400_BAD_REQUEST
      )

    serializer = AvatarSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    image_url = request.build_absolute_uri(user.avatar.url)
    return response.Response(
      {'avatar': image_url},
      status=status.HTTP_200_OK
    )

