from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from quedadas.views import views, user, meeting, chats, challenge, rankings, trophies

urlpatterns = [
    # Views views
    url(r'^$', views.api_root),

    # View meetings
    url(r'^meetings$', meeting.MeetingList.as_view(), name="meeting_list"),
    url(r'^meetings/(?P<pk>[0-9]+)$', meeting.MeetingDetail.as_view(), name="meeting_detail"),
    url(r'^meetings/(?P<meeting>[0-9]+)/tracking/(?P<user>[0-9]+)$', meeting.TrackingView.as_view(),
        name="meeting-track"),
    url(r'^users/meetings$', meeting.UserMeeting.as_view(), name='user-meetings'),
    url(r'^users/(?P<pk>[0-9]+)/meetings$', meeting.UserMeeting.as_view(), name='user-meetings-pk'),
    url(r'^meetings/(?P<pk>[0-9]+)/participants$', meeting.JoinMeeting.as_view(), name="meeting-participants"),
    url(r'^meetings/(?P<pk>[0-9]+)/participants/(?P<usr>[0-9]+)$', meeting.JoinMeeting.as_view(),
        name="meeting-participants-user-pk"),

    # View user
    url(r'^users$', user.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)$', user.UserDetail.as_view(), name='user-detail'),
    url(r'^users/current$', user.CurrentUserView.as_view(), name='current-user'),
    url(r'^users/login$', user.login, name='user-login'),
    url(r'^users/logout$', user.logout),
    url(r'^users/token', user.TokenV.as_view(), name='token'),
    url(r'^users/changePassword$', user.ChangePassword.as_view(), name='change-password'),
    url(r'^users/friends$', user.Friends.as_view()),
    url(r'^users/friends/(?P<pk>[0-9]+)$', user.Friends.as_view(), name='friends'),
    url(r'^users/(?P<pk>[0-9]+)/friends$', user.Friends.as_view(), name='friends-pk'),
    url(r'^users/statistics$', user.Stats.as_view(), name='statistics'),
    url(r'^users/(?P<pk>[0-9]+)/statistics$', user.Stats.as_view(), name='statistics-pk'),
    url(r'^users/(?P<pk>[0-9]+)/ban', user.Ban.as_view(), name='ban-pk'),

    # Chats
    url(r'^chats$', chats.ChatList.as_view(), name='chat-list'),
    url(r'^chats/(?P<pk>[0-9]+)$', chats.ChatDetail.as_view(), name='chat-detail'),
    url(r'^chats/p2p/(?P<pk>[0-9]+)$', chats.ChatP2p.as_view(), name='chat-p2p'),

    # Challenge
    url(r'^challenges$', challenge.ChallengeList.as_view(), name='challenge-list'),
    url(r'^challenges/(?P<pk>[0-9]+)$', challenge.ChallengeDetail.as_view(), name='challenge-detail'),

    # Ranking
    url(r'^rankings$', views.ranking_root, name="rankings-index"),
    url(r'^rankings/users$', rankings.UserList.as_view(), name='ranking-users'),
    url(r'^rankings/zone$', rankings.ZoneList.as_view(), name='ranking-zone'),
    url(r'^rankings/zone/(?P<pk>[0-9]+)$', rankings.ZoneDetail.as_view(), name='zone-detail'),
    url(r'^rankings/zip$', rankings.ZipList.as_view(), name='zip-list'),

    # Tophies
    url(r'^trophies$', trophies.Stats.as_view(), name="trophies"),
    url(r'^trophies/(?P<pk>[0-9]+)$', trophies.Stats.as_view(), name="trophies-pk"),

    # Feed
    url(r'^feed/(?P<pk>[0-9]+)$', user.Feed.as_view(), name="feed-pk"),
    url(r'^feed$', user.Feed.as_view(), name="feed"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
