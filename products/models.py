from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images/")
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