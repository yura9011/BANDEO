# Estado del Proyecto — BANDEO

> Última actualización: 2026-05-13

## Estado actual

**Fase:** MVP funcionando localmente + configurado para deploy en Vercel
**Deploy:** Configurado (pendiente de primer deploy)

## Qué está hecho

- ✅ Directorio público de músicos y bandas (`/`)
- ✅ Perfiles con instrumentos, géneros, ciudad, bio, YouTube, Instagram, Spotify, WhatsApp
- ✅ Crear perfil sin registro (`/create`)
- ✅ Editar perfil con edit token (`/edit/{token}`)
- ✅ Tablón de novedades de bandas (`/bandas`)
- ✅ Publicar novedad con edit token (`/bandas/nuevo`)
- ✅ Geolocalización via Nominatim (lat/lng por ciudad)
- ✅ Links de contacto directo (WhatsApp con mensaje pre-llenado, Instagram, Spotify)
- ✅ Sin sistema de autenticación (email/password eliminados)
- ✅ Base de datos migrada a PostgreSQL (Neon.tech)
- ✅ Configuración de deploy en Vercel (`vercel.json`, `api/index.py`)
- ✅ Connection pool adaptativo (SQLite local / PostgreSQL remoto según DATABASE_URL)

## Qué falta para el MVP real

- [ ] Foto de perfil
- [ ] Buscador/filtros (cuando haya suficiente volumen)
- [ ] Primer deploy a Vercel + configurar variables de entorno

## Decisiones tomadas

- Sin autenticación → edit token único por perfil
- Sin chat interno → contacto directo por WhatsApp/Instagram
- Sin sistema de puntuación → descartado para MVP
- Directorio público → cualquiera puede ver sin registrarse
- Buscador removido de landing → agregar cuando haya volumen
- PostgreSQL (Neon.tech) en producción → SQLite para dev local (según DATABASE_URL)
- Vercel como plataforma de deploy → serverless functions

## Variables de entorno requeridas

| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | Connection string de PostgreSQL (Neon.tech) |
| `ADMIN_USER` | Usuario del panel admin |
| `ADMIN_PASSWORD` | Contraseña del panel admin |
| `ADMIN_SECRET` | Token secreto de sesión admin |

## Archivos clave

- `app/main.py` — rutas
- `app/models/user.py` — modelos (User, Profile, Post, Event)
- `app/database.py` — engine adaptativo SQLite/PostgreSQL
- `app/templates/` — todos los templates HTML
- `vercel.json` — configuración de deploy
- `api/index.py` — entry point serverless
- `requirements.txt` — dependencias
