import requests
from django.conf import settings
from rest_framework import serializers
from .models import Noticias

class NoticiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticias
        fields = '__all__'
        extra_kwargs = {
            'autor_nombre': {'required': False},
            'autor_email': {'required': False},
            'entidad_nombre': {'required': False},
        }

    def validate(self, data):
        autor_id = data.get('autor_id') or getattr(self.instance, 'autor_id', None)
        entidad_id = data.get('entidad_id') or getattr(self.instance, 'entidad_id', None)

        if not autor_id:
            raise serializers.ValidationError({'autor_id': 'Se requiere autor_id para crear la noticia.'})
        if not entidad_id:
            raise serializers.ValidationError({'entidad_id': 'Se requiere entidad_id para crear la noticia.'})

        if self.instance and 'autor_id' not in data and 'entidad_id' not in data:
            return data

        user = self._fetch_usuario(autor_id)
        entidad = self._fetch_entidad(entidad_id)
        perfil = self._fetch_perfil(autor_id, entidad_id)

        if not perfil:
            raise serializers.ValidationError({'entidad_id': 'El usuario no está vinculado a esta entidad.'})

        if not entidad.get('aprobacion_entidad'):
            raise serializers.ValidationError({'entidad_id': 'La entidad no está aprobada para publicar noticias.'})

        data['autor_nombre'] = f"{user.get('nombre', '')} {user.get('apellido', '')}".strip()
        data['autor_email'] = user.get('email')
        data['entidad_nombre'] = entidad.get('nombre_entidad')

        return data

    def _fetch_usuario(self, autor_id):
        url = f"{settings.USUARIOS_SERVICE_URL}/api/usuarios/{autor_id}/"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise serializers.ValidationError({'autor_id': 'Usuario no encontrado en el servicio de usuarios.'})
        return response.json()

    def _fetch_entidad(self, entidad_id):
        url = f"{settings.USUARIOS_SERVICE_URL}/api/entidades/{entidad_id}/"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise serializers.ValidationError({'entidad_id': 'Entidad no encontrada en el servicio de usuarios.'})
        return response.json()

    def _fetch_perfil(self, autor_id, entidad_id):
        url = f"{settings.USUARIOS_SERVICE_URL}/api/perfiles/"
        params = {
            'usuario_perfil': autor_id,
            'entidad_perfil': entidad_id,
            'es_activo': 'true',
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            raise serializers.ValidationError({'entidad_id': 'No se pudo validar la relación usuario-entidad.'})
        perfiles = response.json()
        return perfiles[0] if perfiles else None



