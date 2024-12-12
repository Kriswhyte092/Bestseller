from django.shortcuts import render
from rest_framework import generics, status
from .serializers import NOOSserializer
from .models import NOOS
from rest_framework.views import APIView
from rest_framework.response import Response 


class NOOSview(generics.ListAPIView):
    queryset = NOOS.objects.all()
    serializer_class = NOOSserializer

