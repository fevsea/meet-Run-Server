from django.db import models
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.query_utils import Q


class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(null=False, blank=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True)
    public = models.BooleanField(null=False, blank=False)
    level = models.IntegerField(null=True, blank=True)
    latitude = models.CharField(max_length=10, null=False, blank=False)
    longitude = models.CharField(max_length=10,null=False, blank=False)
    owner = models.ForeignKey('auth.User', related_name='meetings', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='prof')
    question = models.CharField(max_length=100, blank=False, null=False)
    answer = models.CharField(max_length=100, blank=False, null=False)
    postal_code = models.CharField(max_length=5, blank=False, null=False)
    level = models.IntegerField(null=False, blank=False, default=0)
    #other fields

    def get_friends(self):
        user = self.user
        friends = user.friendship_creator_set.friends  # |  user.friend_set.all()
        friends.distinct()

class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="friendship_creator_set")
    friend = models.ForeignKey(User, related_name="friend_set")

    def __str__(self):
        return self.creator.username + " - " + self.friend.username

User.objects.filter()