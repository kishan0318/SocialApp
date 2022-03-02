from dataclasses import fields
from operator import is_
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView,DeleteView
from .forms import RegisterForm,LoginForm
from django.contrib.auth import login,logout,authenticate
from .models import User,Profile,Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .api.serializers import Post_ser,CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

# Create your views here.

class Signup(View):
    def get(self,request):
        f=RegisterForm(None)
        return render(request,'socialapp/home.html',{"data":f})
    def post(self,request):
        f=RegisterForm(request.POST)  
        if f.is_valid():
            data=f.save(commit=False)
            p=f.cleaned_data.get('password')
            data.set_password(p)
            data.save()
            return redirect('login')
        return render(request,'socialapp/home.html',{"data":f})


class AddProfile(LoginRequiredMixin,CreateView):
    login_url='socialapp/login'
    model = Profile
    fields = ['image','address','intrest','dob']
    template_name = 'socialapp/addprofile.html'
    def form_valid(self, form):
        p = self.request.user.id
        a = User.objects.get(pk=p)
        form.instance.u_id = a 
        return super().form_valid(form)


@login_required
def Feeds(request):
    obj=Post.objects.all()
    data=Post_ser(obj,many=True).data
    # obj1=Comment.objects.filter()
    return render(request,'socialapp/show_post.html',{'data':data})


@login_required
def Profile(request):
    return render(request,'socialapp/show_profile.html')


class Signin(View):
    def get(self,request):
        f=LoginForm(None)
        return render(request,'socialapp/login.html',{"data":f})
    def post(self,request):
        f=LoginForm(request.POST)
        if f.is_valid():
            u=f.cleaned_data.get("username") 
            p=f.cleaned_data.get("password")
            ur=authenticate(username=u,password=p)
            nxt=request.GET.get('next')
            if ur:
                login(request,ur)
                if nxt:
                    return redirect(nxt)
                else:
                    return redirect('feeds')
        return render(request,'socialapp/login.html',{"data":f})


def signout(request):
    logout(request)
    return redirect("login")


class AddPost(LoginRequiredMixin,CreateView):
    login_url="socialapp/login"
    model=Post
    fields=['image','message']
    template_name='socialapp/addprofile.html'
    def form_valid(self, form):
        user=self.request.user.id
        a= User.objects.get(pk=user)
        form.instance.userr=a
        return super().form_valid(form)


@login_required
def Myposts(request):
    a=request.user.id
    obj=Post.objects.filter(userr=a)
    return render(request, 'socialapp/editpost.html',{'obj':obj})


@login_required
def Del_post(request,pk):
    obj2=Post.objects.get(id=pk)
    obj2.delete()
    return redirect('myposts')

# def cmntpost(request,*args,**kwargs):
#     if request.method =="POST":
#         name = request.user
#         post1=kwargs.get('pk')
#         print(post1)
#         post1=Post.objects.get(id=Post)
#         comment = request.POST.get('comment1')
#         print(comment)
#         Comment(name=name,post=post1,comments=comment).save()
#         return HttpResponse('done')
#     return render(request,'socialapp/show_post.html')

class Cmntpost(CreateView):
    model = Comment
    fields=['post','comments']
    template_name = 'socialapp/comments_form.html'
    def form_valid(self, form):
        user=self.request.user.id
        a= User.objects.get(pk=user)
        form.instance.name=a
        return super().form_valid(form)

# class AddLikes(LoginRequiredMixin,View):
#     def post(self, request,pk,*args,**kwargs):
#         post=Post.objects.get(pk=pk)
#         is_dislike=False
#         for dislike in post.dislikes.all():
#             if dislike==request.user:
#                 is_dislike=True
#                 break
#         if is_dislike:
#             post.dislikes.remove(request.user)

#         is_like=False

#         for like in post.likes.all():
#             if like==request.user:
#                 is_like=True
#                 break
        
#         if not is_like:
#             post.likes.add(request.user)

#         if is_like:
#             post.like.remove(request.user)

# class AddDislikes(LoginRequiredMixin,View):
#     def post(self, request,pk,*args,**kwargs):
#         post=Post.objects.get(pk=pk)

#         is_like=False

#         for like in post.likes.all():
#             if like==request.user:
#                 is_like=True
#                 break
        
#         if is_like:
#             post.likes.remove(request.user)

#         is_dislike=False

#         for dislikes in post.dislikes.all():
#             if dislikes==request.user:
#                 is_dislike=True
#                 break
#         if not is_dislike:
#              post.dislikes.add(request.user)

#         if is_dislike:
#             post.dislikes.remove(request.user)

