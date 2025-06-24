from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='author_photos/', blank=True, null=True)

    class Meta:
        db_table = 'users_profile'

    def __str__(self):
        return f"{self.user.username}'s profile"