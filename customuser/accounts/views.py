from plistlib import UID
from django.shortcuts import render,redirect
from django.http import BadHeaderError, HttpResponse
from django.db.models.query_utils import Q
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate
from.forms import Registeruser,LoginUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage  
from django.contrib.auth import update_session_auth_hash
from .token import account_activation_token  
from django.template.loader import render_to_string  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django import template
import uuid
from django.contrib import messages

# Create your views here.
def registerform(request):
    fm=Registeruser(request.POST)

    if request.method=='POST':
        # print(request.POST.values, 'requestdata check')
        fm=Registeruser(request.POST)
        if fm.is_valid():
    
            firstname=fm.cleaned_data['firstname']
            username=fm.cleaned_data['username']
            email=fm.cleaned_data['email']
            password=fm.cleaned_data['password']
            mobile=fm.cleaned_data['mobile']
            location=fm.cleaned_data['location']
       
            user=NewUser.objects.create(firstname=firstname,username=username,email=email,password=make_password(password),mobile=mobile,location=location)
            # user = user.save(commit=False) 
            user.is_active=False
            user.save()
            current_site = get_current_site(request)  
            
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = fm.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration') 
            return redirect('login')
        
        else:
            return render(request, 'register.html', {'form':fm})
        
    return render(request,'register.html')


def loginform(request):
    if request.method == 'POST':
        form = LoginUser(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
    
            password = form.cleaned_data.get('password')
        

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # messages.info(request, f"You are now logged in as {username}")
                    return redirect('/homepage/')
                
                       
                else:
                    messages.error(request, "Not active.")
                    return render(request, 'login.html')

                    
            else:
                
                messages.error(request, "Invalid username or password.")
                return render(request, 'login.html')

        else:
            messages.error(request, "Invalid username or password.")
   
    form = LoginUser()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})
    
    
    
def activate(request, uidb64, token):  
   
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        
        user = NewUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, NewUser.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')   
        return redirect('/login')
    
    else:  
        return HttpResponse('Activation link is invalid!')    


def forgotpassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user=NewUser.objects.get(email=email)
        # print(user, ' ma hun user')     
        # if user.exists():
        current_site = get_current_site(request)  
        mail_subject = 'Reset password link has been sent to your email id'  
        message = render_to_string('forgotPM.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user)),  
                'token':account_activation_token.make_token(user),  
            })  
        to_email = email  
        email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
        email.send()  
        return HttpResponse('Please confirm your email address to complete the registration') 
    # else:          
    #     return render(request,'forgot.html')
    # password_reset_form = PasswordResetForm()
    return render(request, 'forgot.html')


def home(request):
    return render(request,'homepage.html')

def confirm(request):
    return render(request,'confirm_register.html')

def ChangePassword(request):
    context={}
    if request.method=='POST':
        current=request.POST['OP']
        new_pass=request.POST['NP']
        passcon = request.POST['CP']        
        user=NewUser.objects.get(email=request.user)
        check=user.check_password(current)

        if check==True:
            if new_pass ==passcon:
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Password changed succesfully')
                return redirect("/login")
            else:
                messages.error(request, "new password and confirm password not matched")
                return render(request,'changepassword.html')
        else:
            messages.error(request, 'Password not changed ')

            return render(request, 'changepassword.html')
                 

    return render(request,'changepassword.html',context)

def ChangePasswordDone(request):
    
    return render(request,'changePD.html')

def index(request):        
    return render(request,'index.html')

def forgotpasswordchange(request):
    context={}
    if request.method=='POST':
        new_pass=request.POST['newpassword']
        con_pass=request.POST['confirmnewpassword']
        user=NewUser.objects.get(email=request.user)
        if new_pass==con_pass:
            user.set_password(new_pass)
            user.save()
            messages.success(request,'New password has been changed')
            return redirect("/login")
        else:
            messages.error(request,'An error occured,try again')
            return render(request,'fps')
            
    return render(request,'forgotpasswordchange.html')



def forgotP(request, uidb64, token):  
   
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = NewUser.objects.get(pk=uid)  

    except(TypeError, ValueError, OverflowError, NewUser.DoesNotExist):  
        print("check")
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save() 
        messages.success(request,'Your password has been changed')   
        return redirect('login/')
    
    
    else:  
        return HttpResponse('An error occured!')    

