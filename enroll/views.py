from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,EditUserProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.models import User

# signup:
def sign_up(request):
    if request.method == "POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
         messages.success(request,'Successfully created')
         fm.save()
    else:
     fm=SignUpForm()
    return render(request,'enroll/signup.html',{'form':fm})

#Login view:
def login(request):
   if request.method=='POST':
      fm=AuthenticationForm(request=request,data=request.POST)
      if fm.is_valid():
        uname=fm.cleaned_data['username']
        pw=fm.cleaned_data['password']
        user=authenticate(username=uname,password=pw)
        if user is not None:
           login(request,user)
           return HttpResponseRedirect('/profile/')
   else:
      fm=AuthenticationForm()
   return render(request,'enroll/userlogin.html',{'form':fm})

#Profile:
def user_profile(request):
   if not request.user.is_authenticated:
      if request.method=="POST":
         if request.user.is_superuser == True: #agar true hai to vo admin hoga
            fm=EditAdminProfileForm(request.POST,instance=request.user)
            users=User.objects.all()
         else:
            fm=EditUserProfileForm(request.POST,instance=request.user)
         if fm.is_valid():
            messages.success(request,"Profile Updated !!")
            fm.save()
      else:
         if request.user.is_superuser == True: #agar true hai to vo admin hoga
            fm=EditAdminProfileForm(instance=request.user)
            users=User.objects.all()
         else:
            fm=EditUserProfileForm(instance=request.user)
            users=None
      return render(request,'enroll/profile.html',{'name':request.user,'form':fm,'users':users})
   else:
      return HttpResponseRedirect('/log/')


#Logout
def user_logout(request):
   logout(request)
   return HttpResponseRedirect('/log/')

#change PW with old pw:
def change_pas(request):
    if request.method=='POST':
      fm=PasswordChangeForm(user=request.user,data=request.POST)
      if fm.is_valid():
         fm.save()
         update_session_auth_hash(request,fm.user)
         messages.success(request,"Password changed successfully")
         return HttpResponseRedirect('/profile/')
    else:
     fm=PasswordChangeForm(user=request.user)
    return render(request,'enroll/changepw.html',{'form':fm})

#without old pw : then use SetPasswordForm instead of PasswordChangeForm.

def user_detail(request,id):
   if request.user.is_authenticated:
      pi=User.objects.get(pk=id)
      fm=EditAdminProfileForm(instance=pi)
      return render(request,'enroll/userdetail.html',{'form':fm})
   else:
      return HttpResponseRedirect('/log/')