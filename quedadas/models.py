from django.db import models
from django.contrib.auth.models import User
from django.db import models



# Create your models here.
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from quedadas import firebase


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
    participants = models.ManyToManyField(User, related_name='meetings_at')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)

class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="friendship_creator_set", null=False, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="friend_set", null=False, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.creator.username + " - " + self.friend.username


class Tracking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    averagespeed = models.FloatField() # m/s
    distance = models.FloatField() # m
    steps = models.IntegerField()
    totalTimeMillis = models.IntegerField() # ms
    calories = models.FloatField() # kcal
    meeting = models.ForeignKey(Meeting, related_name="tracks", null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="tracks", null=False, on_delete=models.CASCADE)


    def __str__(self):
        if self.meeting.title:
            return self.meeting.title
        return "No last meeting"

class RoutePoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    track = models.ForeignKey(Tracking, related_name="routePoints", null=False, on_delete=models.CASCADE)


class Chat(models.Model):
    chatName = models.TextField(null=False, unique=True)
    listUsersChat = models.ManyToManyField(User, related_name="chats")
    type = models.IntegerField()
    meeting = models.ForeignKey(Meeting, null=True, blank=True, on_delete=models.CASCADE)
    lastMessage = models.TextField(null=False)
    lastMessageUserName = models.IntegerField(null=True, blank=True)
    lastDateTime = models.DateTimeField(null=True, blank=True)

    @property
    def num_participiants(self):
        return self.listUsersChat.count()

@receiver(post_save, sender=Tracking, dispatch_uid="update_statistics")
def update_stats(sender, instance, **kwargs):
     stats = instance.user.prof.statistics
     stats.distance += instance.distance
     stats.steps += instance.steps
     stats.totalTimeMillis += instance.totalTimeMillis
     stats.calories += instance.calories
     stats.meetingsCompletats += 1
     stats.lastTracking = instance
     
     if stats.maxDistance < instance.distance:
         stats.maxDistance = instance.distance
     if stats.maxAverageSpeed < instance.averagespeed:
         stats.maxAverageSpeed = instance.averagespeed
     if stats.maxDuration < instance.totalTimeMillis:
         stats.maxDuration = instance.totalTimeMillis
         
     if stats.minDistance > instance.distance or stats.minDistance == 0:
         stats.minDistance = instance.distance
     if stats.minAverageSpeed > instance.averagespeed or stats.averagespeed == 0:
         stats.minAverageSpeed = instance.averagespeed
     if stats.minDuration > instance.totalTimeMillis or stats.totalTimeMillis == 0 :
         stats.minDuration = instance.totalTimeMillis
         
     stats.save()

class Statistics(models.Model):
    distance = models.FloatField(default=0)
    steps = models.IntegerField(default=0)
    totalTimeMillis = models.IntegerField(default=0)
    calories = models.FloatField(default=0)
    meetingsCompletats = models.IntegerField(default=0)
    lastTracking = models.OneToOneField(Tracking, null=True, on_delete=models.SET_NULL)
    maxDistance = models.FloatField(default=0)
    maxAverageSpeed = models.FloatField(default=0)
    maxDuration = models.IntegerField(default=0)
    minDistance = models.FloatField(default=0)
    minAverageSpeed = models.FloatField(default=0)
    minDuration = models.IntegerField(default=0)

    @property
    def averagespeed(self):
        if self.totalTimeMillis == 0:
            return 0
        return float(self.distance/(self.totalTimeMillis/1000))

    def __str__(self):
        if self.prof.user.username:
            return self.prof.user.username
        return "Statistic object with no username"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='prof')
    question = models.CharField(max_length=100, blank=False, null=False)
    answer = models.CharField(max_length=100, blank=False, null=False)
    postal_code = models.CharField(max_length=5, blank=False, null=False)
    level = models.IntegerField(null=False, blank=False, default=0)
    statistics = models.OneToOneField(Statistics, on_delete=models.CASCADE, related_name='prof', null=True, blank=True)
    token = models.CharField(null=True, blank=True, max_length=256)

    def get_friends(self):
        user = self.user
        friends = User.objects.filter(Q(friend_set__creator=user) | Q(friendship_creator_set__friend=user))
        return friends.distinct()

@receiver(post_save, sender=Profile, dispatch_uid="update_stock_count")
def init_statistics(sender, instance, **kwargs):
    if instance.statistics is None:
        statistic = Statistics()
        statistic.save()
        instance.statistics = statistic
        instance.save()


class Challenge(models.Model):
    creator = models.ForeignKey(User, related_name="challenge_creator", null=False, on_delete=models.CASCADE)
    challenged = models.ForeignKey(User, related_name="challenged", null=False, on_delete=models.CASCADE)
    distance = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    creatorBase = models.FloatField(null=True)
    challengedBase = models.FloatField(null=True)
    accepted = models.BooleanField(default=False, blank=True)

    @property
    def creatorDistance(self):
        return self.creator.prof.statistics.distance - self.creatorBase

    @property
    def challengedDistance(self):
        return self.challenged.prof.statistics.distance - self.challengedBase

    def save(self, *args, **kwargs):
        if not self.creatorBase:
            self.creatorBase = self.creator.prof.statistics.distance
        if not self.challengedBase:
            self.challengedBase = self.challenged.prof.statistics.distance

        super(Challenge, self).save( *args, **kwargs)


    def __str__(self):
        return self.creator.username + " <> " + self.challenged.username

@receiver(post_save, sender=Challenge, dispatch_uid="notify_new_challenge")
def notify_user(sender, instance, **kwargs):
    firebase.new_challenge(instance)
