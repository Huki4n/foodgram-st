from django.urls import include, path
from rest_framework import routers

import users

# Assuming users.urls is a module with user-related URLs

# from .views import TagViewSet, IngredientViewSet, RecipeViewSet, CustomUserViewSet

router = routers.DefaultRouter()
# router.register('ingredients', IngredientViewSet, basename='ingredients')
# router.register('recipes', RecipeViewSet, basename='recipes')
# router.register('users', users.urls, basename='users')
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include('users.urls')),
    path('', include('recipes.urls', namespace='recipes')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]