from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import (Menu, Booking)
from .serializers import (MenuSerializer, BookingSerializer)


# Create your views here.
def index(request):
    return render(request, "index.html")

class MenuItemView(ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class SingleMenuItemView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class BookingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.filter()
    serializer_class = BookingSerializer

