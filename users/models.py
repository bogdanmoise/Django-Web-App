from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

IMAGE_MAX_SIZE = 365

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, default='')
    date_joined = models.DateField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='profile_pictures')


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        new_image = Image.open(self.image.path)
        if(new_image.width > IMAGE_MAX_SIZE or new_image.height > IMAGE_MAX_SIZE):
            size = (IMAGE_MAX_SIZE, IMAGE_MAX_SIZE)
            new_image.thumbnail(size)
            new_image.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'