from datetime import datetime

from rest_framework import generics, permissions, status
from .serializers import (
    EventUserSerializer,
    EventSerializer,
    BookingDeleteSerializer,
    BookingAddSerializer,
    RegisterSerializer,
    LoginSerializer,

)

from .models import (
    EventUser,
    Event,
    Booking,
)

from knox.models import AuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout


class UserView(generics.ListCreateAPIView):
    """Get user API"""

    queryset = EventUser.objects.all().exclude(is_staff=True)
    serializer_class = EventUserSerializer


class EventView(generics.ListCreateAPIView):
    """Get spots API"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer




class BookingView(generics.ListCreateAPIView):
    """Make users reservation API"""

    serializer_class = BookingAddSerializer
    queryset = Booking.objects.all()

    def post(self, request, format=None):
        serializer = BookingAddSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response((request.data), status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):

        serializer = BookingDeleteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status = status.HTTP_406_NOT_ACCEPTABLE)


        booking_id = request.data['booking_id']
        if Booking.objects.filter(id=booking_id).exists():
            Booking.objects.get(id=booking_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = Booking.objects.all()
        userid = self.request.query_params.get("userid", None)
        if userid is not None:
            queryset = queryset.filter(reserved_by_id=userid)
        return queryset


class RegisterView(generics.GenericAPIView):
    """User register API"""

    serializer_class = RegisterSerializer
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    """User login API"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        return Response(
            {
                "user": EventUserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    """Get users by token API"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = EventUserSerializer

    def get_object(self):
        return self.request.user
