from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'), 
    path('feedback/', views.feedback, name='feedback'),
    path('news/<int:id>/', views.news, name='news'),
    path('create_article/', views.create_article, name='create_article'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-article/<int:id>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete_article'),

    path('api/', include('blog.api_urls')),
]