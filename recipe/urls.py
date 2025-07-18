"""
URL configuration for recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from recipeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view, name='home'),   # or LoginView.as_view
    path('home/', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('add-recipe/',views.add_recipe, name='add_recipe'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-dishes/<int:pk>/', views.edit_dishes_view, name='edit_dishes'),
    path('delete-recipe/<int:pk>/', views.delete_recipe_view, name='delete_recipe'),
    path('like/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
