from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def Login(request):
    return HttpResponse('Login not implemented')

@csrf_exempt
def Logout(request):
    return HttpResponse('Logout not implemented')

@csrf_exempt
def CreateStory(request):
    return HttpResponse('Create story not implemented')

def ListStories(request):
    return HttpResponse('List stories not implemented')

@csrf_exempt
def DeleteStory(request):
    return HttpResponse('Delete story not implemented')
