from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserUpdateForm,ProfileImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def Register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'user/register.html',{'form':form})

@login_required()
def Profile(request):
    if request.method== "POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileImageForm(request.POST,request.FILES, instance=request.user.profile)
        print(request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Your account has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileImageForm(instance=request.user.profile)

    context={
    'u_form':u_form,
    'p_form':p_form
    }
    return render(request,'user/profile.html',context)