from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetail, PostsListSearch, create_post, PostUpdate, PostDelete

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', PostsListSearch.as_view()),
    path('news/create', create_post),
    path('news/<int:pk>/edit', PostUpdate.as_view()),
    path('articles/create', create_post),
    path('articles/<int:pk>/edit', PostUpdate.as_view()),
    path('news/<int:pk>/delete', PostDelete.as_view()),
    path('articles/<int:pk>/delete', PostDelete.as_view()),
]

