from django.shortcuts import render
from rest_framework import generics
from .serializers import NOOSserializer
from .models import NOOS


class NOOSview(generics.ListAPIView):
    queryset = NOOS.objects.all()
    serializer_class = NOOSserializer

