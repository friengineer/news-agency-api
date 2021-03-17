from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from stories.models import Story
import json
from datetime import datetime

@require_POST
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

@require_POST
@csrf_exempt
def Logout(request):
    try:
        logout(request)

        response = HttpResponse('You have successfully logged out, goodbye.', content_type='text/plain')
    except:
        response = HttpResponseServerError('Logout failed and you have not been logged out.', content_type='text/plain')

    return response

@require_POST
@csrf_exempt
def CreateStory(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unable to post story because user is not logged in.', content_type='text/plain', status=503)

    try:
        data = json.loads(request.body.decode('UTF-8'))
        story = Story(headline=data['headline'],
                      category=data['category'],
                      region=data['region'],
                      author=request.user,
                      publication_date=timezone.now(),
                      details=data['details'])

        story.full_clean()
        story.save()

        response = HttpResponse(content_type='text/plain', status=201)
    except ValidationError as e:
        message = 'Unable to post story because of the following reasons:'

        if 'headline' in e.message_dict:
            message += '\nHeadline: ' + e.message_dict['headline'][0]

        if 'category' in e.message_dict:
            message += '\nCategory: ' + e.message_dict['category'][0]

        if 'region' in e.message_dict:
            message += '\nRegion: ' + e.message_dict['region'][0]

        if 'details' in e.message_dict:
            message += '\nDetails: ' + e.message_dict['details'][0]

        response = HttpResponse(message, content_type='text/plain', status=503)
    except:
        response = HttpResponse('An unknown error occurred and your story has not been posted.', content_type='text/plain', status=503)

    return response

@require_GET
def ListStories(request):
    data = json.loads(request.body.decode('UTF-8'))

    results = Story.objects.all()

    if data['story_cat'] != '*':
        results = results.filter(category=data['story_cat'])

    if data['story_region'] != '*':
        results = results.filter(region=data['story_region'])

    if data['story_date'] != '*':
        date = datetime.strptime(data['story_date'], '%d/%m/%Y')
        results = results.filter(publication_date__gte=timezone.make_aware(date, is_dst=False))

    if not results.exists():
        return HttpResponseNotFound('No stories found that match the supplied criteria.', content_type='text/plain')

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

@require_POST
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
