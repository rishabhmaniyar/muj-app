"""emastratapis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views
from .views import LevelsView

urlpatterns = [
    path('', views.LevelsView.as_view(), name='levels_list'),
    path('start', views.start_tracking, name='start_tracking'),  # Use the function-based view directly
    path('create_map', views.create_tracker, name='create_track_map'),  # Use the function-based view directly
    path('create', views.LevelsView.as_view(), name='levels_create'),
    path('<int:pk>/', views.LevelsView.as_view(), name='levels_detail'),
    path('<int:pk>/update/', views.LevelsView.as_view(), name='levels_update'),
    path('<int:pk>/delete/', views.LevelsView.as_view(), name='levels_delete'),
]
