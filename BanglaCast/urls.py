"""
URL configuration for BanglaCast project.

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
from django.urls import path, include
from BC import views as a_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', a_views.Explore, name='Explore'),
    path('home', a_views.home, name='home'),
    path('signUpCreator', a_views.signUpCreator, name='signUpCreator'),
    path('signUpListener', a_views.signUpListener, name='signUpListener'),
    path('login', a_views.loginUser, name='login'),
    path('logOut', a_views.logOut, name='logOut'),
    path('upload_episode/', a_views.upload_episode, name='upload_episode'),
    path('delete_epi/<str:id>', a_views.delete_epi, name='delete_epi'),
    path('player/<str:id>', a_views.player, name='player'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)