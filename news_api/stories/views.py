from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from stories.models import Story
import json
from datetime import datetime

@csrf_exempt
def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return HttpResponse('You are logged in, welcome back!', content_type='text/plain')
    else:
        return HttpResponse('Failed login. The credentials supplied are incorrect.', content_type='text/plain', status=401)

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
        data = json.loads(request.body.decode('UTF-8'))

        Story.objects.create(headline=data['headline'],
                             category=data['category'],
                             region=data['region'],
                             author=request.user,
                             publication_date=timezone.now(),
                             details=data['details'])

        response = HttpResponse(content_type='text/plain', status=201)
    except:
        response = HttpResponse('An error occurred and your story has not been posted.', content_type='text/plain', status=503)

    return response

def ListStories(request):
    data = json.loads(request.body.decode('UTF-8'))

    results = Story.objects.all()

    if data['story_cat'] != '*':
        results = results.filter(category=data['story_cat'])

    if data['story_region'] != '*':
        results = results.filter(region=data['story_region'])

    if data['story_date'] != '*':
        results = results.filter(publication_date__gte=datetime.strptime(data['story_date'], '%d/%m/%Y'))

    if not results.exists():
        return HttpResponseNotFound('No stories have been found that match the supplied criteria.', content_type='text/plain')
    
    results = results.values()
    jsonResults = []

    for story in results:
        author = User.objects.get(pk=story['author_id'])
        name = author.first_name + ' ' + author.last_name

        date = story['publication_date'].strftime('%d/%m/%Y')

        jsonResults.append({'key': str(story['id']),
                            'headline': story['headline'],
                            'story_cat': story['category'],
                            'story_region': story['region'],
                            'author': name,
                            'story_date': date,
                            'story_details': story['details']})

    payload = {'stories': jsonResults}

    return JsonResponse(payload)

@csrf_exempt
def DeleteStory(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unable to delete story because user is not logged in.', content_type='text/plain', status=503)

    try:
        data = json.loads(request.body.decode('UTF-8'))
        story = Story.objects.get(pk=data['story_key'])
        story.delete()

        response = HttpResponse(content_type='text/plain', status=201)
    except:
        response = HttpResponse('An error occurred and the story has not been deleted.', content_type='text/plain', status=503)

    return response
