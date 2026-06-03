from rest_framework import serializers
from .models import Noticias
from django.contrib.auth.hashers import make_password

class NoticiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticias
        fields = '__all__'



