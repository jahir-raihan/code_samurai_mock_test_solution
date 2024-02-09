from rest_framework import serializers
from .models import *


class UserCSSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCS
        fields = ['user_id', 'user_name', 'balance']


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ['station_id', 'station_name', 'longitude', 'latitude']


class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = ['train_id', 'train_name', 'capacity']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        stop_first = Stops.objects.first()
        stop_end = Stops.objects.last()
        service_start = stop_first.departure_time.strftime('%H:%M')
        service_end = stop_end.arrival_time.strftime('%H:%M')
        num_stations = Stops.objects.count()

        data['service_start'] = service_start
        data['service_end'] = service_end
        data['num_stations'] = num_stations

        return data


class StopsSerializerEx(serializers.ModelSerializer):
    
    class Meta:
        model = Stops
        fields = ['train_id', 'arrival_time', 'departure_time']
