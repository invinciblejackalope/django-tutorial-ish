from django.db import models
from django.utils import timezone

# Post model
class Post(models.Model):
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    timestamp = models.DateTimeField('date posted')
    mod_time = models.DateTimeField('date last modified')
    # what to return if str() is called on a Post object (used for testing)
    def __str__(self):
        return self.values()
