from django.db import models
from django.contrib.auth.models import User

class credentials(models.Model):
    name = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    key = models.BinaryField(max_length=200, null=False)
    user_id = models.CharField(max_length=600, null=True, blank=True)
    password = models.CharField(max_length=600, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    


    def __str__(self):
        return self.name.username
