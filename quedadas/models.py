from django.db import models

# Create your models here.

class Quedada(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    public = models.BooleanField()

    def __str__(self):
        if self.title == '':
            return "Quedada sense títol"
        else:
            return self.title

    class Meta:
        ordering = ('created',)