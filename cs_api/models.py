from django.db import models

# Create your models here.


class UserCS(models.Model):
    user_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=50)
    balance = models.IntegerField()


class Station(models.Model):
    station_id = models.IntegerField()
    station_name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()


class Train(models.Model):
    train_id = models.IntegerField()
    train_name = models.CharField(max_length=100)
    capacity = models.IntegerField()


class Stops(models.Model):
    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True, blank=True)
    station_id = models.ForeignKey(Station, related_name='station', on_delete=models.SET_NULL, null=True, blank=True)
    arrival_time = models.TimeField(null=True,blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    fare = models.IntegerField(default=0)


class TicketId(models.Model):
    ticket_id = models.IntegerField(default=100)




