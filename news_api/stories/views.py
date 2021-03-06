from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return HttpResponse('You are logged in, welcome back!', content_type='text/plain')
    else:
        return HttpResponse('Failed login. The credentials supplied are incorrect.', content_type='text/plain', status=503)

@csrf_exempt
def Logout(request):
    try:
        logout(request)

        response = HttpResponse('You have successfully logged out, goodbye.', content_type='text/plain')
    except:
        response = HttpResponse('Logout failed and you have not been logged out.', content_type='text/plain', status=503)

    return response

@csrf_exempt
def CreateStory(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unable to post story because user is not logged in.', content_type='text/plain', status=503)

    try:
        response = HttpResponse('Your story has been posted.', content_type='text/plain', status=201)
    except:
        response = HttpResponse('An error occurred and your story has not been posted.', content_type='text/plain', status=503)

    return response

def ListStories(request):
    return HttpResponse('List stories not implemented')

@csrf_exempt
def DeleteStory(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unable to delete story because user is not logged in.', content_type='text/plain', status=503)

    try:
        response = HttpResponse('The story has been deleted.', content_type='text/plain', status=201)
    except:
        response = HttpResponse('An error occurred and the story has not been deleted.', content_type='text/plain', status=503)

    return response
