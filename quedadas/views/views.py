# coding=utf-8
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    return Response({
        'meetings': reverse('meeting_list', request=request),
        'users': reverse('user-list', request=request),
        'chats': reverse('chat-list', request=request),
        'challenges': reverse('challenge-list', request=request),
        'rankings': reverse('rankings-index', request=request),
        'trophies': reverse('trophies', request=request),
        'feed': reverse('feed', request=request),
        'admin': ''.join(['http://', get_current_site(request).domain, "/admin"]),
        'docs': reverse('docs', request=request),
    })


@api_view(['GET'])
def ranking_root(request):
    return Response({
        'zone': reverse('ranking-zone', request=request),
        'users': reverse('ranking-users', request=request),
        'zips': reverse('zip-list', request=request),

    })
