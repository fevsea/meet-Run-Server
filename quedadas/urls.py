from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from quedadas import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^users/login', views.login),
    url(r'^users/logout', views.logout),
    url(r'^test$', views.TestList.as_view(), name="test_list"),
    url(r'^meetings$', views.MeetingList.as_view(), name="meeting_list"),
    url(r'^meetings/(?P<pk>[0-9]+)$', views.MeetingDetail.as_view(), name="meeting_detail"),
    url(r'^meetings/(?P<pk>[0-9]+)/participants$', views.JoinMeeting.as_view(), name="join_meeting"),
    url(r'^users$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/(?P<pk>[0-9]+)/meetings$', views.UserMeeting.as_view(), name='user-meetings'),
    url(r'^users/(?P<pk>[0-9]+)/friends$', views.Friends.as_view(), name='priends-pk'),
    url(r'^users/friends$', views.Friends.as_view(), name='firends'),
    url(r'^users/friends/(?P<pk>[0-9]+)$', views.Friends.as_view(), name='add-firends'),
    url(r'^users/current$', views.CurrentUserView.as_view(), name='current-user')
]

urlpatterns = format_suffix_patterns(urlpatterns)
