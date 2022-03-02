from math import perm
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import User,LikePost
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *


class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSer
    permission_classes = [AllowAny, ]


class RegisterView1(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = RegisterSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Hey,you are registerd succesfully', 'data': data}, status=HTTP_200_OK)
        return Response(status=HTTP_406_NOT_ACCEPTABLE)


class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSer(data=request.data)
        if serializer.is_valid():
            return Response({'Success': 'login successfully', 'data': serializer.data}, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # print(request.user.id)
        serializer = ProfileSer(data=request.data, context={
                                'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "profile added successfully", 'data': serializer.data}, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        queryset = Profile.objects.filter(u_id=user)
        serializer = ProfileSer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self,request):
        user=request.user
        obj=Profile.objects.filter(u_id=user)
        serializer=ProfileSer(instance=obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'update successfully'},status=HTTP_200_OK)
        return Response({'msg':'update UNsuccessfull'})


class CRDPostApiView(APIView):
    permission_classes =[IsAuthenticated,]

    def get(self, request):
        user = request.user
        queryset = Post.objects.filter(userr=user)
        serializer = PostSer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        ser = PostSer(data=request.data, context={'user': request.user})
        if ser.is_valid():
            ser.save()
            return Response({'success':'post sent successfully','data':ser.data}, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user=request.user
        obj=Post.objects.filter(userr=user)
        obj.delete()
        return Response({'Message':'All Posts Deleted Successfully'},status=HTTP_200_OK)


class DeleteAPIView(APIView):
    permission_classes =[IsAuthenticated,]
    def delete(self,request,**kwargs):
        try:
            Post.objects.get(pk=self.kwargs.get('pk'),userr=request.user)
            return Response({'Success':'user deleted successfully'},status=HTTP_200_OK)
        
        except Exception as e:
            return Response({'Error':str(e)},status=HTTP_400_BAD_REQUEST)

class CommentsApiView(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,*args,**kwargs):
        user=request.user
        post_id=request.data.get('post')
        try:
            x=Post.objects.get(id=post_id)
        except:
            return Response({'Message':'Invalid post or does not exist'},status=HTTP_400_BAD_REQUEST)
        if x:
            Comment.objects.create(post=x,comments=request.data.get('comment'),name=user,date_added=request.data.get('date')).save()
            x1=Comment.objects.filter(post=x).count()
            return Response({'message': 'Comment added successfully','comments':x1},status=200)
        else:
            return Response({'message':'Something went Wrong or try again'},status=404)


class LikeAPIView(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user = request.user
        id=request.data.get('post_id')
        try:
            posts = Post.objects.get(id=id)
        except:
            return Response({'message' : 'Post Not found'},status=HTTP_400_BAD_REQUEST)
        liked= False
        like = LikePost.objects.filter(user=user,post=posts)
        if like:
            like.delete()
        else:
            liked = True
            LikePost.objects.create(user=user,post=posts)
        obj = LikePost.objects.filter(post=posts).count()
        return Response({'Likes':obj},status=HTTP_200_OK)


class FriendAPIView(APIView):
    permission_classes =[IsAuthenticated,]
    def post(self,request,*args,**kwargs):
        user=request.user
        id=request.data.get('to_user')
        date=request.data.get('on_date')
        # to_user=User.objects.get(id=id)
        try:
            x=User.objects.get(id=id)
        except:
            return Response({'error':'Not found'},status=HTTP_404_NOT_FOUND)
        requested=False
        request=Friends.objects.filter(from_user=user,to_user=x)
        if request:
            request.delete()
        else:
            requested=True
            Friends.objects.create(from_user=user,to_user=x,on_date=date)
            # return Response({'Error':'Request Sent successfully'},status=HTTP_404_NOT_FOUND)
        return Response({'message':'Request Sent successfully','data':requested},status=HTTP_200_OK)
     

  

    

 