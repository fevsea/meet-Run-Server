# coding=utf-8
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    return Response({
        'meetings': reverse('meeting_list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'chats': reverse('chat-list', request=request, format=format),
        'challenges': reverse('challenge-list', request=request, format=format),
        'rankings': reverse('rankings-index', request=request, format=format),
        'trophies': reverse('trophies', request=request, format=format),
        'feed': reverse('feed', request=request, format=format),
        'admin': ''.join(['http://', get_current_site(request).domain, "/admin"]),
        'docs': reverse('docs', request=request, format=format),
    })


@api_view(['GET'])
def ranking_root(request):
    return Response({
        'zone': reverse('ranking-zone', request=request, format=format),
        'users': reverse('ranking-users', request=request, format=format),
        'zips': reverse('zip-list', request=request, format=format),

    })
