from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import Mock, patch

from .models import Noticias


class NoticiasAPITest(APITestCase):
    @patch('noticias_app.serializers.requests.get')
    def test_create_noticia_requires_entidad_aprobada_y_perfil_activo(self, mock_get):
        user_response = Mock(status_code=200, json=Mock(return_value={
            'id': 1,
            'nombre': 'Ana',
            'apellido': 'Perez',
            'email': 'ana@example.com',
        }))
        entidad_response = Mock(status_code=200, json=Mock(return_value={
            'id': 10,
            'nombre_entidad': 'Refugio Sanos',
            'aprobacion_entidad': True,
        }))
        perfil_response = Mock(status_code=200, json=Mock(return_value=[{
            'id': 5,
            'usuario_perfil': 1,
            'entidad_perfil': 10,
            'rol_entidad': 'Trabajador',
            'es_activo': True,
        }]))
        mock_get.side_effect = [user_response, entidad_response, perfil_response]

        data = {
            'titulo': 'Nueva campaña',
            'contenido': 'Noticias sobre la campaña de adopción.',
            'autor_id': 1,
            'entidad_id': 10,
        }

        response = self.client.post('/api/noticias/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['autor_nombre'], 'Ana Perez')
        self.assertEqual(response.data['entidad_nombre'], 'Refugio Sanos')

    @patch('noticias_app.views.requests.post')
    def test_delete_noticia_requiere_admin(self, mock_post):
        noticia = Noticias.objects.create(
            titulo='Test',
            contenido='Contenido test',
            autor_id=1,
            autor_nombre='Ana Perez',
            autor_email='ana@example.com',
            entidad_id=10,
            entidad_nombre='Refugio Sanos',
        )
        mock_post.return_value = Mock(status_code=200, json=Mock(return_value={'rol': 'Colaborador'}))

        response = self.client.delete(f'/api/noticias/{noticia.id}/', HTTP_AUTHORIZATION='Bearer token')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('noticias_app.views.requests.post')
    def test_delete_noticia_admin_succeeds(self, mock_post):
        noticia = Noticias.objects.create(
            titulo='Test',
            contenido='Contenido test',
            autor_id=1,
            autor_nombre='Ana Perez',
            autor_email='ana@example.com',
            entidad_id=10,
            entidad_nombre='Refugio Sanos',
        )
        mock_post.return_value = Mock(status_code=200, json=Mock(return_value={'rol': 'Admin'}))

        response = self.client.delete(f'/api/noticias/{noticia.id}/', HTTP_AUTHORIZATION='Bearer token')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('noticias_app.views.requests.post')
    def test_update_noticia_guarda_editor(self, mock_post):
        noticia = Noticias.objects.create(
            titulo='Original',
            contenido='Contenido original',
            autor_id=1,
            autor_nombre='Ana Perez',
            autor_email='ana@example.com',
            entidad_id=10,
            entidad_nombre='Refugio Sanos',
        )
        mock_post.return_value = Mock(status_code=200, json=Mock(return_value={
            'user_id': 2,
            'email': 'editor@example.com',
            'nombre': 'Pedro',
            'apellido': 'Gonzalez',
            'rol': 'Admin',
        }))

        response = self.client.patch(
            f'/api/noticias/{noticia.id}/',
            {'contenido': 'Contenido actualizado'},
            format='json',
            HTTP_AUTHORIZATION='Bearer token',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['editado_por_nombre'], 'Pedro Gonzalez')
        self.assertEqual(response.data['editado_por_email'], 'editor@example.com')
        self.assertIsNotNone(response.data['editado_por_fecha'])

