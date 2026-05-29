# Bandeo

Bandeo es un directorio público para músicos y bandas. Permite publicar un perfil simple, mostrar instrumentos, géneros, ciudad, enlaces y medios, y facilitar el contacto directo a través de plataformas externas como WhatsApp, Instagram, Spotify y YouTube.

El producto está pensado para reducir fricción: cualquier persona puede explorar perfiles sin crear una cuenta, y cada músico o banda puede administrar su publicación mediante un enlace privado de edición.

## Alcance del producto

Bandeo incluye:

- Directorio público de perfiles de músicos y bandas.
- Creación de perfiles sin registro tradicional.
- Edición de perfiles mediante enlace privado.
- Página pública de perfil con bio, ubicación, instrumentos, géneros, medios y contacto.
- Tablón de novedades para publicaciones breves de bandas.
- Calendario de fechas y presentaciones.
- Panel de administración para revisión operativa.
- Historial recuperable de cambios relevantes.

La aplicación no incluye chat interno, sistema de puntuación ni autenticación completa de usuarios. El contacto ocurre fuera de Bandeo, mediante los enlaces publicados por cada perfil.

## Stack técnico

- Python
- FastAPI
- SQLModel
- PostgreSQL
- Jinja2
- Tailwind CSS

## Estructura principal

```text
app/
  main.py              Rutas y handlers de la aplicación
  database.py          Configuración de base de datos y sesiones
  audit.py             Historial recuperable de cambios
  models/user.py       Modelos de datos
  templates/           Vistas HTML renderizadas en servidor
  static/              Recursos públicos
api/
  index.py             Entry point serverless
requirements.txt       Dependencias de Python
vercel.json            Configuración de despliegue
```

## Configuración y datos

La configuración de ejecución se administra mediante variables de entorno. Este repositorio no debe contener valores reales, credenciales, archivos `.env`, bases de datos, logs, caches, datos de producción ni notas operativas privadas.

El repositorio debe representar el código de la aplicación y su documentación pública. La información local de trabajo, instrucciones para agentes, detalles privados de despliegue y datos runtime quedan fuera del control de versiones.

## Seguridad de datos

Bandeo registra un historial recuperable para las operaciones principales de escritura. El historial guarda snapshots antes y después de ediciones, creaciones, acciones de moderación y eliminaciones. Los tokens privados de edición no se guardan en esos snapshots.

## Estado

Bandeo es un MVP activo. El foco actual es consolidar el directorio público, preservar correctamente los datos publicados por usuarios y mejorar el flujo operativo de administración sin agregar complejidad innecesaria al producto.
