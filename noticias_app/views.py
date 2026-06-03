from django.shortcuts import render
from .models import Noticias

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import NoticiasSerializer

from rest_framework.decorators import api_view
import jwt, time
from django.conf import settings
from django.contrib.auth.hashers import check_password
# Create your views here.

def lista_noticias(request):
    noticias = Noticias.objects.all()
    return render(request, 'noticias.html', {'noticias': noticias})


class NoticiasViewSet(viewsets.ModelViewSet):
    queryset = Noticias.objects.all()
    serializer_class = NoticiasSerializer

    def get_queryset(self):
        queryset = Noticias.objects.all()
        return queryset




