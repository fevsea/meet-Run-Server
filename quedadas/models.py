from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from quedadas.controllers import meetingCtrl, firebaseCtrl, rankingsCtrl, trophyCtrl


class Zone(models.Model):
    distance = models.IntegerField(null=False, blank=True, default=0)
    zip = models.CharField(max_length=5, blank=False, null=False, primary_key=True)
    average = models.FloatField(default=0)

    def __str__(self):
        return self.zip


class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(null=False, blank=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True)
    public = models.BooleanField(null=False, blank=False)
    level = models.IntegerField(null=False, blank=True, default=0)
    latitude = models.CharField(max_length=10, null=False, blank=False)
    longitude = models.CharField(max_length=10, null=False, blank=False)
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
    averagespeed = models.FloatField()  # m/s
    distance = models.FloatField()  # m
    steps = models.IntegerField()
    totalTimeMillis = models.IntegerField()  # ms
    calories = models.FloatField()  # kcal
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
    meeting = models.OneToOneField(Meeting, null=True, blank=True, on_delete=models.CASCADE, related_name="chat_r")
    lastMessage = models.TextField(null=False, blank=True)
    lastMessageUserName = models.TextField(null=True, blank=True)
    lastDateTime = models.DateTimeField(null=True, blank=True)

    @property
    def num_participiants(self):
        return self.listUsersChat.count()


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
    challenges = models.IntegerField(default=0)

    @property
    def averagespeed(self):
        if self.totalTimeMillis == 0:
            return 0
        return float(self.distance / (self.totalTimeMillis / 1000))

    def __str__(self):
        if self.prof.user.username:
            return self.prof.user.username
        return "Statistic object with no username"

@receiver(post_save, sender=Tracking, dispatch_uid="update_statistics")
def update_stats(sender, instance, **kwargs):
    meetingCtrl.update_stats(sender, instance, **kwargs)
    rankingsCtrl.update_zone_ranking(sender, instance, **kwargs)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='prof')
    question = models.CharField(max_length=100, blank=False, null=False)
    answer = models.CharField(max_length=100, blank=False, null=False)
    postal_code = models.ForeignKey(Zone, related_name="members", on_delete=models.CASCADE)
    level = models.IntegerField(null=False, blank=False, default=0)
    statistics = models.OneToOneField(Statistics, on_delete=models.CASCADE, related_name='prof', null=True, blank=True)
    token = models.CharField(null=True, blank=True, max_length=256)
    ban_count = models.ManyToManyField(User)
    ban_date = models.DateTimeField(null=True, blank=True)

    def get_friends(self):
        user = self.user
        friends = User.objects.filter(Q(friend_set__creator=user) | Q(friendship_creator_set__friend=user))
        return friends.distinct()

    def save(self, *args, **kwargs):
        old = Profile.objects.get(pk=self.pk).level
        new = self.level
        if old != new:
            trophyCtrl.check_level(self.statistics, old, new)
        super(Profile, self).save(*args, **kwargs)

    @property
    def friend_number(self):
        user = self.user
        friends = User.objects.filter(Q(friend_set__accepted=True) | Q(friendship_creator_set__accepted=True))
        friends = friends.filter(Q(friend_set__creator=user) | Q(friendship_creator_set__friend=user)).distinct()
        return friends.count()



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
    completed = models.BooleanField(default=False, blank=True)

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

        super(Challenge, self).save(*args, **kwargs)

    def check_completion(self):
        if self.deadline < timezone.now():
            firebaseCtrl.challenge_finalized(self)
            self.completed = True
        elif self.challengedDistance >= self.distance:
            firebaseCtrl.challenge_won(self, self.challenged)
            firebaseCtrl.challenge_lost(self, self.creator)
            stats = self.challenged.prof.statistics
            trophyCtrl.check_challenges(stats, stats.challenges, stats.challenges + 1)
            self.challenged.prof.statistics.challenges += 1
            self.completed = True
        elif self.creatorDistance >= self.distance:
            firebaseCtrl.challenge_lost(self, self.challenged)
            firebaseCtrl.challenge_won(self, self.creator)
            stats = self.creator.prof.statistics
            trophyCtrl.check_challenges(stats, stats.challenges, stats.challenges + 1)
            self.creator.prof.statistics.challenges += 1
            self.completed = True
        self.save()

    def __str__(self):
        return self.creator.username + " <> " + self.challenged.username

    def notify_accepted(self):
        firebaseCtrl.challenge_accepted(self)


@receiver(post_save, sender=Tracking, dispatch_uid="update_challenge_statistics")
def update_challenge_statistics(sender, instance, **kwargs):
    user = instance.user
    challenges_creator = user.challenge_creator.filter(completed=False)
    challenges_challenged = user.challenged.filter(completed=False)
    for challenge in (challenges_creator | challenges_challenged).distinct():
        challenge.check_completion()


@receiver(post_save, sender=Challenge, dispatch_uid="notify_new_challenge")
def notify_user(sender, instance, **kwargs):
    firebaseCtrl.new_challenge(instance)
