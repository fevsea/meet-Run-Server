from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from quedadas.views import views, user, meeting, chats, challenge, rankings

urlpatterns = [
    # Views views
    url(r'^$', views.api_root),

    # View meetings
    url(r'^meetings$', meeting.MeetingList.as_view(), name="meeting_list"),
    url(r'^meetings/(?P<pk>[0-9]+)$', meeting.MeetingDetail.as_view(), name="meeting_detail"),
    url(r'^meetings/(?P<meeting>[0-9]+)/tracking/(?P<user>[0-9]+)$', meeting.TrackingView.as_view(),
        name="meeting_track"),
    url(r'^users/meetings$', meeting.UserMeeting.as_view(), name='user-meetings'),
    url(r'^users/(?P<pk>[0-9]+)/meetings$', meeting.UserMeeting.as_view(), name='user-meetings-pk'),
    url(r'^meetings/(?P<pk>[0-9]+)/participants$', meeting.JoinMeeting.as_view(), name="join_meeting"),
    url(r'^meetings/(?P<pk>[0-9]+)/participants/(?P<usr>[0-9]+)$', meeting.JoinMeeting.as_view(),
        name="join_meeting_pk"),

    # View user
    url(r'^users$', user.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)$', user.UserDetail.as_view(), name='user-detail'),
    url(r'^users/current$', user.CurrentUserView.as_view(), name='current-user'),
    url(r'^users/login$', user.login),
    url(r'^users/logout$', user.logout),
    url(r'^users/token', user.TokenV.as_view(), name='token'),
    url(r'^users/changePassword$', user.changePassword.as_view(), name='change-password'),
    url(r'^users/friends$', user.Friends.as_view(), name='firends'),
    url(r'^users/friends/(?P<pk>[0-9]+)$', user.Friends.as_view(), name='add-firends'),
    url(r'^users/(?P<pk>[0-9]+)/friends$', user.Friends.as_view(), name='priends-pk'),
    url(r'^users/statistics$', user.Stats.as_view(), name='statistics'),
    url(r'^users/(?P<pk>[0-9]+)/statistics$', user.Stats.as_view(), name='statistics-pk'),

    # Chats
    url(r'^chats$', chats.ChatList.as_view(), name='chat-list'),
    url(r'^chats/(?P<pk>[0-9]+)$', chats.ChatDetail.as_view(), name='chat-detail'),
    url(r'^chats/p2p/(?P<pk>[0-9]+)$', chats.ChatP2p.as_view(), name='chat-p2p'),

    # Challenge
    url(r'^challenges$', challenge.ChallengeList.as_view(), name='challenge-list'),
    url(r'^challenges/(?P<pk>[0-9]+)$', challenge.ChallengeDetail.as_view(), name='challenge-detail'),

    # Ranking
    url(r'^rankings$', views.ranking_root, name="rankings-index"),
    url(r'^rankings/zone', rankings.ZoneList.as_view(), name='ranking-zone'),
    url(r'^rankings/zip', rankings.ZipList.as_view(), name='zip-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
