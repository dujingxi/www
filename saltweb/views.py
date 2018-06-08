
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import LoginForm, MailForm
from django.core.mail import send_mail

# from django.views.decorators.http import require_safe


# @login_required(redirect_field_name='this_next')
@login_required
def index_view(request):
    return render(request, 'index.html')

# login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:    
                login(request, user)
                return redirect(index_view)
                # ss = request.session.get_expiry_date()
                return render(request, 'test.html')
            else:
                return render(request, 'login.html', {"errmsg": 'Invalid username or password.'})
        else:
            return render(request, 'login.html', {'errmsg': 'Invalid forms data.'})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect(user_login)

def test(request):
    ss = request.session
    return render(request, 'test.html', {'ss': ss.clear()})





def send_msg(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            recvs = [sender]
            send_mail(subject, message, sender, recvs)
            return HttpResponse("subject: %s, message: %s, sender: %s"%(subject, message, sender))
        else:
            return HttpResponse("not valid")
    else:
        return HttpResponse("not post")