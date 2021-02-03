from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=1000, default="")
    bought = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

class Item(models.Model):
    name = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    tag = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="images/")
    best = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'