from django.shortcuts import render
from django.utils import timezone
from .models import Noticias

from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import NoticiasSerializer

import requests
from django.conf import settings


def lista_noticias(request):
    noticias = Noticias.objects.all()
    return render(request, 'noticias.html', {'noticias': noticias})


class NoticiasViewSet(viewsets.ModelViewSet):
    queryset = Noticias.objects.all()
    serializer_class = NoticiasSerializer

    def get_queryset(self):
        return Noticias.objects.all()

    def perform_update(self, serializer):
        editor = self._get_current_user_info(self.request)
        if editor:
            serializer.save(
                editado_por_nombre=f"{editor.get('nombre', '')} {editor.get('apellido', '')}".strip(),
                editado_por_email=editor.get('email'),
                editado_por_fecha=timezone.now(),
            )
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not self._request_is_admin(request):
            return Response(
                {'detail': 'Solo usuarios con rol Admin pueden eliminar noticias.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def _request_is_admin(self, request):
        token = self._get_bearer_token(request)
        if not token:
            return False
        auth_url = f"{settings.AUTH_SERVICE_URL.rstrip('/')}/validate-token/"
        try:
            response = requests.post(auth_url, json={'token': token}, timeout=5)
            if response.status_code != 200:
                return False
            return response.json().get('rol') == 'Admin'
        except requests.RequestException:
            return False

    def _get_current_user_info(self, request):
        token = self._get_bearer_token(request)
        if not token:
            return None
        auth_url = f"{settings.AUTH_SERVICE_URL.rstrip('/')}/validate-token/"
        try:
            response = requests.post(auth_url, json={'token': token}, timeout=5)
            if response.status_code != 200:
                return None
            return response.json()
        except requests.RequestException:
            return None

    def _get_bearer_token(self, request):
        authorization = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION', '')
        if isinstance(authorization, str) and authorization.startswith('Bearer '):
            return authorization.split(' ', 1)[1]
        return None




