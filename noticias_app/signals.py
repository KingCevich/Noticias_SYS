from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Noticias

@receiver(post_migrate)
def create_default_noticias(sender, **kwargs):
    if sender.name != 'noticias_app':
        return
    if Noticias.objects.exists():
        return

    # IDs de usuarios y entidades que YA existen en usuarios_serv (creados por su propio signal)
    noticias_data = [
        {
            "titulo": "Nueva campaña de adopción en Refugio Demo",
            "contenido": "El Refugio Demo ha lanzado una campaña para promover la adopción responsable durante todo el mes. Puedes visitarlos en Santiago Centro. Esta es una oportunidad única para darle un hogar a un animal necesitado. El refugio cuenta con perros y gatos de todas las edades, todos desparasitados y vacunados.",
            "imagen_url": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=200&fit=crop",
            "autor_id": 2,           # Admin Refugio (refugio@demo.com)
            "autor_nombre": "Admin Refugio",
            "autor_email": "refugio@demo.com",
            "entidad_id": 2,         # Refugio Demo
            "entidad_nombre": "Refugio Demo",
        },
        {
            "titulo": "Veterinaria Bío Bío ofrece descuentos en vacunación",
            "contenido": "Durante junio, la Veterinaria Bío Bío ofrece un 20% de descuento en el plan de vacunación anual. Agenda tu hora llamando al +56988888888. El plan incluye vacuna quíntuple, antirrábica y desparasitación interna.",
            "imagen_url": "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=400&h=200&fit=crop",
            "autor_id": 11,          # Admin Bío Bío (vetbiobio@demo.com)
            "autor_nombre": "Admin Bío Bío",
            "autor_email": "vetbiobio@demo.com",
            "entidad_id": 11,
            "entidad_nombre": "Veterinaria Bío Bío",
        },
        {
            "titulo": "Municipalidad de Las Condes realizará operativo de esterilización",
            "contenido": "El próximo sábado 15 de junio se realizará un operativo gratuito en la Plaza de Armas. Inscripciones en el link: https://example.com/inscripciones. Se atenderán hasta 50 mascotas por orden de llegada. Los dueños deben llevar carnet de identidad y certificado de tenencia responsable.",
            "imagen_url": "https://images.unsplash.com/photo-1582015181274-5d8ee5a5e1a5?w=400&h=200&fit=crop",
            "autor_id": 4,           # Admin Municipalidad (municipalidad@demo.com)
            "autor_nombre": "Admin Municipalidad",
            "autor_email": "municipalidad@demo.com",
            "entidad_id": 4,
            "entidad_nombre": "Municipalidad Demo",
        },
        {
            "titulo": "Fundación Huella Animal busca voluntarios",
            "contenido": "Se necesitan voluntarios para cuidar a los animales los fines de semana. Interesados escribir al correo voluntarios@huellaanimal.cl. Las tareas incluyen limpieza de jaulas, paseo de perros y ayuda en eventos de adopción.",
            "imagen_url": "",
            "autor_id": 10,          # Admin Huella (huella@demo.com)
            "autor_nombre": "Admin Huella",
            "autor_email": "huella@demo.com",
            "entidad_id": 10,
            "entidad_nombre": "Fundación Huella Animal",
        },
    ]

    for item in noticias_data:
        Noticias.objects.create(**item)

    print("<<<<Noticias de prueba creadas>>>>")