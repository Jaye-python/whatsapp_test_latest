from django.db import models
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

fsize = settings.FILE_SIZE

class UserManager(BaseUserManager):
    def create_user(self, email, password= None, ):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(
            email = self.normalize_email(email),
              )
        user.set_password(password)
        user.save(using = self.db)
        return user

    def create_superuser(self, email, password=None,):
        if not email:
            raise ValueError('Email is Required')
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
              )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self.db)
        return user
    
    
class CustomUser(AbstractUser):

    username = None
    first_name = models.CharField(max_length=20 )
    email = models.EmailField(_('email address'),db_index=True, unique=True, help_text='Please input your email address which will be verified before login.')
    chat_room = models.ForeignKey('ChatRoom', on_delete=models.SET_NULL, null=True, db_index=True, )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'


    class Meta:
        ordering = ['-date_joined']
        
    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name
            
            
def validate_file_size(value):
    filesize= value.size
    sz = filesize/1000
    
    if filesize > fsize:
        raise ValidationError(f"The maximum file size allowed is {fsize/1000}kb. You file is {sz}kb")
    else:
        return value

    
class ChatRoom(models.Model):
    MAX_MEMBERS = 1

    room = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(CustomUser)

    def clean(self):
        if self.members.count() > self.MAX_MEMBERS:
            raise ValidationError(f"Chat room can have at most {self.MAX_MEMBERS} members.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    
class Message(models.Model):
    
    def picture_upload(instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{instance.created_by}_{instance.chatroom}_{instance.created_at}.{ext}'
        return os.path.join('picture', filename)
    
    def video_upload(instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{instance.created_by}_{instance.chatroom}_{instance.created_at}.{ext}'
        return os.path.join('video', filename)
    
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    text = models.TextField()
    picture = models.ImageField(upload_to= 'picture', null=True, blank = True,)
    video = models.FileField(upload_to= 'video', null=True, blank = True, )
    created_at = models.DateTimeField(auto_now_add=True)