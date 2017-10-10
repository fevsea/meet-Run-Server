from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from rest_framework import routers
from quedadas import views

urlpatterns = [
    #url(r'^$', views.root),
    url(r'^quedadas/$', views.quedada_list),
    url(r'^quedadas/(?P<pk>[0-9]+)/$', views.quedada_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)