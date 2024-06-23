from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetail, PostsListSearch, create_post, PostUpdate, PostDelete,  \
    BaseRegisterView, upgrade_me
from django.contrib.auth.views import LoginView, LogoutView

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
    path('signup', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('news/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade')
]

