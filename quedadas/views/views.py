# coding=utf-8
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.sites.shortcuts import get_current_site

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'meetings': reverse('meeting_list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'admin': ''.join(['http://', get_current_site(request).domain, "/admin"]),
        'docs': reverse('docs', request=request, format=format),
    })
