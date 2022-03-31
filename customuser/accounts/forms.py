from django import forms

from .models import NewUser

class Registeruser(forms.Form):
    firstname=forms.CharField()
    username=forms.CharField()
    email=forms.EmailField()
    mobile=forms.IntegerField()
    password=forms.CharField()
    location=forms.CharField()
    
    
    def clean_username(self):
        valusername=self.cleaned_data.get('username')
        if len(valusername)<4:
            raise forms.ValidationError('Enter compatible username')
        return valusername
    
    def clean_email(self):
        valemail=self.cleaned_data.get('email')
        if len(valemail)<7:
            raise forms.ValidationError('Enter comapatible email') 
        if NewUser.objects.filter(email=valemail).exists():
            raise forms.ValidationError('Email already exist') 
        
        return valemail
        
    def clean_mobile(self):
        valmobile=self.cleaned_data.get('mobile')
        if valmobile<=12:
            raise forms.ValidationError('Enter mobile number less than 12 digits')
        if NewUser.objects.filter(mobile=valmobile).exists():
            raise forms.ValidationError('number already exist') 
        
        return valmobile
 
class  LoginUser(forms.Form):  
    username=forms.CharField()
    password=forms.CharField()
    
class ChangePassword(forms.Form):
      old_password=forms.CharField()
      new_password=forms.CharField()
      reenter_password=forms.CharField()
      def clean(self):
          new_password=self.cleaned_data.get('new_password')
          reenter_password=self.cleaned_data.get('reenter_password')
          old_password=self.cleaned_data.get('old_password')
          if new_password and new_password!=reenter_password or new_password==old_password:
                  return self.cleaned_data 
              
        
        
    
     