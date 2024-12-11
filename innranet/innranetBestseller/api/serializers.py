from rest_framework import serializers
from .models import NOOS

class NOOSserializer(serializers.ModelSerializer):
    class Meta:
        model = NOOS
        fields = ('id', 'itemCard', 'itemName')

