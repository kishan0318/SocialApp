from django.urls import path
from .views import *

app_name='socialapp'

urlpatterns =[
    path('register',RegisterView1.as_view(),name='register'),
    path('register1',RegisterView.as_view(),name='RegisterView'),
    path('login',LoginAPIView.as_view(),name='LoginView'),
    path('add_profile',ProfileApiView.as_view(),name='add_profile'),
    path('post',CRDPostApiView.as_view(),name='post'),
    path('post/<int:pk>',CRDPostApiView.as_view(),name='post'),
    path('delete/<int:pk>',DeleteAPIView.as_view(),name='delete'),
    path('add_comments',CommentsApiView.as_view(),name='comment'),
    path('like',LikeAPIView.as_view(),name='like'),
    path('send_request',FriendAPIView.as_view(),name='send_request'),
]