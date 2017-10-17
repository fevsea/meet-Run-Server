from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from rest_framework import routers
from quedadas import views

urlpatterns = [
    #url(r'^$', views.root),
    url(r'^meetings/$', views.quedada_list),
    url(r'^meetings/(?P<pk>[0-9]+)/$', views.meeting_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)