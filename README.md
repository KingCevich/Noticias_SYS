# 📰 noticias_serv

Microservicio de publicación y gestión de noticias del sistema SanosYSalvos. Permite a entidades aprobadas publicar noticias y avisos relacionados con mascotas, campañas de adopción y novedades de la plataforma.

**Puerto:** `8004`

---

## Responsabilidades

- Publicar y gestionar noticias creadas por entidades aprobadas
- Validar que el autor tenga perfil activo en una entidad aprobada antes de publicar
- Registrar quién editó una noticia y cuándo
- Restringir la eliminación de noticias a usuarios con rol Admin

---

## Modelos

### `Noticias`

| Campo | Tipo | Descripción |
|---|---|---|
| `titulo` | CharField | Título de la noticia |
| `contenido` | TextField | Contenido completo |
| `imagen_url` | URLField | URL de imagen ilustrativa (opcional) |
| `autor_id` | PositiveIntegerField | ID del usuario autor (referencia a usuarios_serv) |
| `autor_nombre` | CharField | Nombre del autor (guardado localmente) |
| `autor_email` | EmailField | Email del autor (guardado localmente) |
| `entidad_id` | PositiveIntegerField | ID de la entidad publicadora |
| `entidad_nombre` | CharField | Nombre de la entidad (guardado localmente) |
| `fecha_publicacion` | DateTimeField | Fecha de publicación automática |
| `editado_por_nombre` | CharField | Nombre del editor (si fue modificada) |
| `editado_por_email` | EmailField | Email del editor |
| `editado_por_fecha` | DateTimeField | Fecha de la última edición |

---

## Endpoints

| Método | URL | Auth requerida | Descripción |
|---|---|---|---|
| GET | `/api/noticias/` | No | Listar todas las noticias |
| POST | `/api/noticias/` | Sí (entidad aprobada) | Crear una nueva noticia |
| GET | `/api/noticias/{id}/` | No | Obtener una noticia por ID |
| PATCH | `/api/noticias/{id}/` | Sí (Admin) | Actualizar una noticia (guarda editor) |
| DELETE | `/api/noticias/{id}/` | Sí (Admin) | Eliminar una noticia |

> **Nota:** Al crear una noticia, el serializer valida automáticamente contra `usuarios_serv` que el autor tenga perfil activo en una entidad aprobada.

> Se puede utilizar Thunder o Postman para las peticiones API: http://127.0.0.1:8004/

---

## Tests

Los tests usan `@patch` para simular llamadas a `usuarios_serv` sin necesitar que esté corriendo.

- `test_create_noticia_requires_entidad_aprobada_y_perfil_activo` — Verifica que solo entidades aprobadas con perfil activo pueden publicar noticias
- `test_delete_noticia_requiere_admin` — Verifica que un usuario sin rol Admin no puede eliminar noticias (403)
- `test_delete_noticia_admin_succeeds` — Verifica que un Admin puede eliminar noticias (204)
- `test_update_noticia_guarda_editor` — Verifica que al editar una noticia se guardan los datos del editor

```bash
cd noticias_serv
python manage.py test
```

---

## Levantar el servicio

```bash
cd noticias_serv
python manage.py migrate
python manage.py runserver 8004
```

> **Nota:** Requiere que `usuarios_serv` esté corriendo en el puerto 8000 para validar entidades y perfiles al crear noticias, y `auth_serv` en el puerto 8001 para validar tokens en operaciones de escritura.