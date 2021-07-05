from cryptography.fernet import Fernet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msg
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import customUserForm, credentialsForm
from .decorators import unautherize
from .models import credentials
import json



@unautherize
def createUser(request):
    if request.method == "POST":
        form = customUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            msg.success(request, 'User Created!!')
        return HttpResponse('User Created!!')
    else:
        form = customUserForm()
        context = {'form':form}
        return render(request, 'NewDisplay/signup.html', context)
# NewDisplay/
@unautherize
def userLogin(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            msg.error(request, "Username & Password Didn't Match!")
            return HttpResponseRedirect('./')
    else:
        return render(request, 'NewDisplay/login.html')

@login_required(login_url='userLogin')
def userLogout(request):
    logout(request)
    return redirect('userLogin')

def encryptData(form, **kwargs):
    print('inside encrypt')
    raw_username = form.cleaned_data['user_id'].encode('utf-8')
    raw_password = form.cleaned_data['password'].encode('utf-8')
    key = Fernet.generate_key() #this is your "password"
    cipher_suite = Fernet(key)
    username = cipher_suite.encrypt(raw_username).decode('utf-8')
    password = cipher_suite.encrypt(raw_password).decode('utf-8')
    encrytedDict = {'key':key, 'username':username, 'password':password}
    return encrytedDict

def decryptData(obj):
    username = obj.user_id.encode('utf-8')
    key = obj.key
    cipher_suite = Fernet(key)
    password = obj.password.encode('utf-8')
    raw_username = cipher_suite.decrypt(username)
    raw_password = cipher_suite.decrypt(password)
    # print(raw_password, raw_username)
    return {'username':raw_username.decode('utf-8'), 'password':raw_password.decode('utf-8')}

@login_required(login_url='userLogin')
def generate_Data(request):
    if request.method=='POST':
        form = credentialsForm(request.POST)
        # print(form)
        if form.is_valid():
            # print(form.cleaned_data.get('user_id'))
            data = encryptData(form)
            new_data = credentials(
                name=request.user,
                key=data['key'],
                user_id=data['username'],
                password=data['password'],
                description=form.cleaned_data['description'],
            )
            new_data.save()
            return redirect('dashboard')
        # else:
        #     return HttpResponse("<h1>Oops!\nSomething Went Wrong!</h1>")
    else:
        form = credentialsForm()
        context = {'form':form, 'edit':False}
        return render(request, 'NewDisplay/generate_password.html', context)

@login_required(login_url='userLogin')
def dashboard(request):
    data = credentials.objects.filter(name=request.user.id).order_by('-id')
    # sendToken(request)
    if request.method == 'POST':
        new = data.values('id','user_id', 'password', 'description', 'last_updated')
        context = [x for x in new]
        return JsonResponse(context, safe=False)
    context = {'data':data}
    return render(request, 'NewDisplay/dashboard.html',context)

@login_required(login_url='userLogin')
def decode(request):
    if request.method == "POST":
        id = json.load(request)['id']
        obj = credentials.objects.get(id=id)
        if obj.name.id == request.user.id:
            rawData = decryptData(obj)
    # return HttpResponse(f'<h1>Your Details:-\t{decoded_values["username"]}\t{decoded_values["password"]}</h1>')
    return JsonResponse(rawData)

@login_required(login_url='userLogin')
def editData(request, pk):
    obj = credentials.objects.filter(id=pk)[0]
    if obj.name.id == request.user.id:
        if request.method=='POST':
            form = credentialsForm(request.POST, instance=obj)
            if form.is_valid():
                cipher = encryptData(form)
                encrypted_form = form.save(commit=False)
                encrypted_form.user_id, encrypted_form.password = cipher['username'], cipher['password']
                encrypted_form.key = cipher['key']
                encrypted_form.save()
                return redirect('dashboard')
        else:
            edited_data = decryptData(obj)
            form = credentialsForm(instance=obj)
            # print(form.fields['user_id'])
            # form.base_fields['user_id'].value = edited_data['username']
            context = {'form':form, 'data':edited_data, 'edit':True}
            return render(request, 'NewDisplay/generate_password.html', context)
    else:
        return HttpResponse('<h1>404 Page Not Found</h1>')

@login_required(login_url='userLogin')
def deleteData(request):
    if request.method == 'POST':
        requested_id = json.load(request)['id']
        obj = credentials.objects.get(id=requested_id)
        if obj.name.id == request.user.id:
            obj.delete()
            return JsonResponse({'result':'Sucessfully Deleted'})
    else:
        return JsonResponse({'result':'Invalid Request'})
