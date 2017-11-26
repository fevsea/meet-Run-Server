from django.db import models
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    userName = models.ForeignKey(User, null=False, related_name='chatA')
    friendUsername = models.ForeignKey(User, null=False, related_name='chatB')
    last_message = models.TextField(null=False)
    last_time = models.DateTimeField(null=True)
    username_message = models.BooleanField(null=False, default=True)
    last_hour = models.CharField(max_length=30, null=False)


    class Meta:
        unique_together = ('userName', 'friendUsername')

@receiver(post_save, sender=Tracking, dispatch_uid="update_statistics")
def update_stock(sender, instance, **kwargs):
     stats = instance.user.prof.statistics
     stats.distance += instance.distance/1000
     stats.steps += instance.steps
     stats.totalTimeMillis += instance.totalTimeMillis
     stats.calories += instance.calories
     stats.meetingsCompletats += 1
     stats.lastTracking = instance
     stats.save()

class Statistics(models.Model):
    distance = models.FloatField(default=0) # km from m
    steps = models.IntegerField(default=0)
    totalTimeMillis = models.IntegerField(default=0)
    calories = models.FloatField(default=0)
    meetingsCompletats = models.IntegerField(default=0)
    lastTracking = models.OneToOneField(Tracking, null=True)

    @property
    def averagespeed(self):
        if self.totalTimeMillis == 0:
            return 0
        return float(self.distance/(self.totalTimeMillis/3600000))

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


