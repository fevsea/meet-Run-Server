from django.db import models

# Create your models here.

class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(null=False, blank=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True)
    public = models.BooleanField(null=False, blank=False)
    level = models.IntegerField(null=True, blank=False)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)
