"""socialproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from socialapp.views import *
from . import settings
from django.conf.urls.static import static

app_name='socialapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",Signup.as_view(),name='signup'),
    path('add_profile',AddProfile.as_view(),name='add_profile'),
    path('addposts',AddPost.as_view(),name='posts'),
    path('login',Signin.as_view(),name='login'),
    path('profile',Profile,name='profile'),
    path('deletepost/<int:pk>',Del_post,name='deletepost'),
    path('signout',signout,name='logout'),
    path('feeds',Feeds,name='feeds'),
     path('comments/',Cmntpost.as_view(),name='comments'),
    path('myposts',Myposts,name='myposts'),
    # path('cmntpost',Cmntpost.as_view(),name='cmntpost'),
    path('api-auth/', include('rest_framework.urls')),
    path("api/",include('socialapp.api.urls',namespace='socialapp')),
    
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
