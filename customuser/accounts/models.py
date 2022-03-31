from pyexpat import model
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):
    
    def create_user(self,email,password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))  #validator
        
        email = self.normalize_email(email)
        user=self.model(email=email,password=password,**other_fields)
        user.set_password(password)
        user.save()
        return user
    
    
            
    def create_superuser(self,email,password, **other_fields):  
        other_fields.setdefault('is_staff',True)  
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        
        
        if other_fields.get('is_staff')is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            ) 
                    
        if other_fields.get('is_superuser')is not True:
                raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            ) 
         
        return self.create_user(email,password,**other_fields)           
                
           
    

class NewUser(AbstractBaseUser,PermissionsMixin):
    
    email=models.EmailField(_('email address'),unique=True)
    username=models.CharField(max_length=150,unique=False)
    firstname=models.CharField(max_length=150,default='Enter name')
    start_date=models.DateTimeField(default=timezone.now)
    about=models.TextField(_('about'),max_length=500,blank=True)
    mobile=models.CharField(max_length=30,default='enter mobile')
    location=models.CharField(max_length=30,default='enter location')
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)


    objects = CustomAccountManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    
    def __str__(self):
        return self.email