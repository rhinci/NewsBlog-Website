from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ArticleApi, CommentApi, register_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'articles', ArticleApi, basename='articles')
router.register(r'comments', CommentApi, basename='comments')


articles_router = routers.NestedSimpleRouter(router, r'articles', lookup='article')
articles_router.register(r'comments', CommentApi, basename='article-comments')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', register_user, name='api_register'),
    path('', include(articles_router.urls)),
]