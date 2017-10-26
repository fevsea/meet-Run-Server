from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from quedadas import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^login', views.login),
    url(r'^test/$', views.TestList.as_view(), name="test_list"),
    url(r'^meetings/$', views.MeetingList.as_view(), name="meeting_list"),
    url(r'^meetings/(?P<pk>[0-9]+)/$', views.MeetingDetail.as_view(), name="meeting_detail"),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/current/$', views.CurrentUserView.as_view(), name='current-user')
]

urlpatterns = format_suffix_patterns(urlpatterns)