from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserCS, Station, Train, Stops, TicketId
from .serializer import UserCSSerializer, StationSerializer, TrainSerializer, StopsSerializerEx
from django.db.models import Q


class UsersApiView(APIView):

    """
    View for api endpoints of book.
    """

    def get(self, request, wallet_id):

        try:
            user = UserCS.objects.get(user_id=wallet_id)

            data = {
                "wallet_id": wallet_id,
                "balance": user.balance,
                "wallet_user": {
                    "user_id": user.user_id,
                    "user_name": user.user_name
                }
            }

            return Response(data, status=status.HTTP_200_OK)


        except:
            return Response({"message": f"wallet with id: {wallet_id} was not found"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        post_data = request.data

        user = UserCS(
            user_id=post_data['user_id'],
            user_name=post_data['user_name'],
            balance=float(post_data['balance'])
        )

        user.save()

        serialized_data = UserCSSerializer(user, many=False)

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def put(self, request, wallet_id):

        try:
            user = UserCS.objects.get(user_id=wallet_id)
            put_data = request.data

            recharge_amount = int(put_data['recharge'])
            if not 100 <= recharge_amount <= 10000:
                return Response({"message": f"invalid amount: {recharge_amount}"},
                                status=status.HTTP_400_BAD_REQUEST)

            user.balance += recharge_amount
            user.save()

            data = {
                "wallet_id": wallet_id,
                "balance": user.balance,
                "wallet_user": {
                    "user_id": user.user_id,
                    "user_name": user.user_name
                }
            }
            return Response(data, status=status.HTTP_200_OK)


        except:
            return Response({"message": f"wallet with id: {wallet_id} was not found"},
                            status=status.HTTP_404_NOT_FOUND)


class StationsApiView(APIView):

    def get(self, request):

        stations = Station.objects.all().order_by('station_id')

        serialized_data = StationSerializer(stations, many=True)

        return Response({"stations": serialized_data.data}, status=status.HTTP_200_OK)
    def post(self, request):

        post_data = request.data

        station = Station(
            station_id=post_data['station_id'],
            station_name=post_data['station_name'],
            longitude=float(post_data['longitude']),
            latitude=float(post_data['latitude'])
        )

        station.save()

        serialized_data = StationSerializer(station, many=False)

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


class TrainsApiView(APIView):

    def get(self, request, station_id):

        try:
            station = Station.objects.get(station_id=station_id)

            stops = Stops.objects.filter(station_id=station_id).order_by('departure_time').order_by('arrival_time')
            serialized_data = StopsSerializerEx(stops, many=True)

            return Response({"station_id": station_id, "trains": serialized_data.data},
                            status=status.HTTP_200_OK)

        except:
            return Response({"message": f"station with id: {station_id} was not found"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        post_data = request.data

        train = Train(
            train_id=int(post_data['train_id']),
            train_name=post_data['train_name'],
            capacity=int(post_data['capacity'])
        )
        train.save()

        for data in post_data['stops']:
            try:
                station = Station.objects.get(pk=data['station_id'])
            except:
                station = None

            stop = Stops(
                train=train,
                station_id=station,
                arrival_time=data['arrival_time'],
                departure_time=data['departure_time'],
                fare=int(data['fare'])
            )
            stop.save()

        serialized_data = TrainSerializer(train, many=False)

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


class TicketsApiView(APIView):

    def get(self, request):
        pass

    def post(self, request):

        data = request.data

        user = UserCS.objects.get(user_id=int(data['wallet_id']))
        station_from = Station.objects.get(station_id=int(data['station_from']))
        station_to = Station.objects.get(station_id=int(data['station_to']))

        time_after = datetime.strptime(data['time_after'], '%H:%M').time()

        try:
            start_stop = Stops.objects.filter(
                Q(station_id=station_from.station_id) & Q(departure_time__gte=time_after)
            ).order_by('departure_time').first()

            if start_stop.departure_time < time_after:
                raise Exception

            end_stop = Stops.objects.filter(
                Q(station_id=station_to.station_id) & Q(arrival_time__gte=time_after)
            ).order_by('arrival_time').first()

            if end_stop.arrival_time < time_after:
                raise Exception
        except:
            return Response({"message": f"no ticket available for station:"
                                        f" {station_from.station_id} to station:{station_to.station_id}"},
                            status=status.HTTP_403_FORBIDDEN)

        stops = Stops.objects.filter(
            Q(arrival_time__gt=time_after) & Q(station_id__lt=station_to.station_id) &
            Q(arrival_time__lt=end_stop.arrival_time)
        ).order_by('arrival_time')

        cost = 0
        for stp_data in stops:
            cost += stp_data.fare

        if cost > user.balance:
            shortage_amount = cost - user.balance
            return Response({"message": f"recharge amount: {shortage_amount} to purchase the ticket"},
                            status=status.HTTP_402_PAYMENT_REQUIRED)

        user.balance -= cost
        user.save()

        try:
            ticket_id = TicketId.objects.get(id=1)
        except:
            ticket_id = TicketId()
            ticket_id.save()

        ticket_id.ticket_id += 1
        ticket_id.save()

        response_data = {
            "ticket_id": ticket_id.ticket_id,
            "balance": user.balance,
            "wallet_id": user.user_id,
        }

        stop_data = [
            {
                "station_id": data['station_from'],
                "train_id": start_stop.train.train_id,
                "departure_time": start_stop.departure_time,
                "arrival_time": None
            }

        ]
        for stp in stops:

            dic = {
                "station_id": stp.station_id.station_id,
                "train_id": stp.train.train_id,
                "departure_time": stp.departure_time,
                "arrival_time": stp.arrival_time
            }
            stop_data.append(dic)

        dic = {
            "station_id": data['station_to'],
            "train_id": end_stop.train.train_id,
            "departure_time": None,
            "arrival_time": end_stop.arrival_time
        }
        stop_data.append(dic)
        response_data["stations"] = stop_data

        return Response(response_data, status=status.HTTP_201_CREATED)







