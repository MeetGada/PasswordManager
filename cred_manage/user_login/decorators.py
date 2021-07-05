from django.shortcuts import redirect
from .models import credentials
# from django.http import HttpResponse

def unautherize(view_func):
    def check_auth(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return check_auth

def getOwner(view_func):
    def check_auth(request, *args, **kwargs):
        print(request)
        if credentials.objects.filter(id=id)[0] == request.user.id:
            return view_func(request, id, **kwargs)
        else:
            return redirect('dashboard')
    return check_auth