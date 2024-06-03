from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetail

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),

]