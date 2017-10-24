from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from rest_framework import routers
from quedadas import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^meetings/$', views.MeetingList.as_view(), name="meeting_list"),
    url(r'^meetings/(?P<pk>[0-9]+)/$', views.MeetingDetail.as_view(), name="meeting_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)