from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt
def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return HttpResponse('You are logged in, welcome back!', content_type='text/plain')
    else:
        return HttpResponse('Failed login. The credentials supplied are incorrect', content_type='text/plain', status=503)

@csrf_exempt
def Logout(request):
    try:
        logout(request)

        return HttpResponse('You have successfully logged out, goodbye.', content_type='text/plain')
    except:
        return HttpResponse('Logout failed and you have not been logged out', content_type='text/plain', status=503)

@csrf_exempt
def CreateStory(request):
    return HttpResponse('Create story not implemented')

def ListStories(request):
    return HttpResponse('List stories not implemented')

@csrf_exempt
def DeleteStory(request):
    return HttpResponse('Delete story not implemented')
