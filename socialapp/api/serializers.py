from email.mime import message
from pyexpat import model
from django.forms import CharField, DateField, FileField
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField
from socialapp.models import Post, Comment, User,Profile,LikePost,Friends
from rest_framework.serializers import *
from rest_framework_jwt.settings import api_settings
# from rest_framework_jwt.settings import api_settings
from django.views.decorators.csrf import csrf_exempt

class CommentSerializer(ModelSerializer):
    # comments=SerializerMethodField()
    # date_added=SerializerMethodField
    # def get_comments(self,object):
    #     try:
    #         return object.comments
    #     except:
    #         return None
    class Meta:
        model = Comment
        fields = '__all__'

class Post_ser(ModelSerializer):
    image = SerializerMethodField()
    user = SerializerMethodField()
    comments = SerializerMethodField()
    date_added = SerializerMethodField()
    name = SerializerMethodField()

    def get_image(self, object):
        try:
            return object.image.url
        except:
            return None

    def get_user(self, object):
        try:
            return object.userr
        except:
            return []

    def get_comments(self, object):
        try:
            qs = Comment.objects.filter(post=object)
            return CommentSerializer(qs, many=True).data
        except:
            return []

    def get_name(self, object):
        try:
            qs = Comment.objects.filter(post=object)
            return CommentSerializer(qs, many=True).data
        except:
            return []

    def get_date_added(self, object):
        try:
            qs = Comment.objects.filter(post=object)
            return CommentSerializer(qs, many=True).data
        except:
            return []

    class Meta:
        model = Post
        fields = "__all__"
        include = ('comments', 'name', 'date_added')

class RegisterSer(ModelSerializer):
    username = CharField(error_messages={
                         'required': 'Please enter a username', 'blank': 'username can`t be blank'})
    password = CharField(error_messages={
                         'required': 'Please enter a password', 'blank': 'password can`t be blank'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class LoginSer(Serializer):
    username=CharField(error_messages={'required':'Email key is required','blank':'Email is required'})
    password=CharField(error_messages={'required':'Password key is required','blank':'Password is required'})
    token=CharField(read_only=True, required=False)

    def validate(self,data):
        qs=User.objects.filter(username=data.get('username'))
        if not qs.exists():
            raise ValidationError('No account with this username')
        user=qs.first()
        if user.check_password(data.get('password'))==False:
            raise ValidationError('Invalid Password')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data['token']='JWT'+str(token)
        return data


class ProfileSer(Serializer):
    image =FileField(error_messages={'required':'image key is required','blank':'image field can`t be blank is required'})
    address=CharField(error_messages={'required':'address key is required','blank':'address field can`t be blank is required'})
    intrest=CharField(error_messages={'required':'intrest key is required','blank':'intrest field can`t be blank is required'})
    dob=CharField()
    def create(self,data):
        Profile.objects.create(u_id=self.context.get('user'),image=data.get('image'),address=data.get('address'),intrest=data.get('intrest'),dob=data.get('dob')).save()
        return data


class PostSer(Serializer):
    image =FileField(error_messages={'required':False,'blank':True})
    message =CharField(error_messages={'required':'message key is required','blank':True})
    def create(self, data):
        Post.objects.create(userr=self.context.get('user'),image=data.get('image'),message=data.get('message')).save()
        return data

class CommentSer(ModelSerializer):
    class Meta:
        model= Comment
        fields="__all__"


class likeSerializer(ModelSerializer):
    class Meta:
        model=LikePost
        fields=('__all__')

class FriendsSer(ModelSerializer):
    class Meta:
        model=Friends
        fields=('__all__')


class FriendsSer1(Serializer):
    on_date=DateField()
    from_user=CharField(error_messages={'required':'from_user key is required','blank':'from_user field can`t be blank is required'})
    is_accepted=BooleanField()
    def update(self,instance,validated_data):
        instance.on_date = validated_data.get('on_date')
        instance.from_user = User.objects.get(id=validated_data.get('from_user'))
        instance.to_user=self.context.get('user')
        instance.is_accepted=validated_data.get('is_accepted')
        if instance.is_accepted==True:
            instance.save()
        else: 
            instance.delete()
        return validated_data 