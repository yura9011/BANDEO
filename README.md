# Bandeo

Directorio de músicos y bandas. Publicás tu perfil, te encontramos.

## Variables de entorno

Crear un archivo `.env` en la raiz del proyecto:

```
ADMIN_USER=
ADMIN_PASSWORD=
ADMIN_SECRET=
```

## Correr localmente

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Abre en `http://127.0.0.1:8000`

## Cargar datos de prueba

```bash
python seed_db.py
python seed_events.py
```

## Estructura

```
app/
  main.py          rutas
  models/user.py   User, Profile, Post, Event
  database.py      engine y sesion
  utils.py         geocoding, tokens, links
  templates/       HTML (Jinja2 + Tailwind)
  static/          assets
seed_db.py         perfiles de prueba
seed_events.py     eventos de prueba
requirements.txt
```

## Paginas

| URL | Descripcion |
|-----|-------------|
| / | Directorio de perfiles |
| /create | Crear perfil |
| /edit/{token} | Editar perfil |
| /profile/{id} | Ver perfil publico |
| /bandas | Tablon de novedades |
| /bandas/nuevo | Publicar novedad |
| /fechas | Calendario de fechas |
| /fechas/nueva | Agregar fecha |

## Stack

- Python / FastAPI
- SQLite / SQLModel
- Jinja2 / Tailwind CSS
- Geocoding via OpenStreetMap Nominatim
