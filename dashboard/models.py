from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    city_of_origin = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100)

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
