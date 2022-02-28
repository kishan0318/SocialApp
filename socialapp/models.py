from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model):
    u_id=models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.FileField(null=True, blank=True)
    address= models.TextField(max_length=1000)
    intrest=models.CharField(max_length=100)
    dob=models.DateField()

    def get_absolute_url(self):
        return reverse('profile')


class Post(models.Model):
    userr = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(null=True, blank=True)
    message = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('posts')


class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    def get_absolute_url(self):
        return reverse('feeds')

    def __str__(self):
        return f'user{self.name.username} @ {self.date_added}'


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_date=models.DateTimeField(auto_now_add=True)
    
    @property
    def user_count(self):
        return self.post.count


class Friends(models.Model):
    from_user=models.ForeignKey(User, related_name='from_user',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User, related_name='to_user',on_delete=models.CASCADE)
    on_date=models.DateTimeField(auto_now_add=True)

