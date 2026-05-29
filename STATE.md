# Estado del Proyecto — BANDEO

> Última actualización: 2026-05-28

## Estado actual

**Fase:** MVP funcionando en producción (Vercel + Neon.tech)
**Deploy:** ✅ Activo

## Qué está hecho

- ✅ Directorio público de músicos y bandas (`/`)
- ✅ Perfiles con instrumentos, géneros, ciudad, bio, YouTube, Instagram, Spotify, WhatsApp
- ✅ Crear perfil sin registro (`/create`)
- ✅ Editar perfil con edit token (`/edit/{token}`)
- ✅ Tablón de novedades de bandas (`/bandas`)
- ✅ Publicar novedad con edit token (`/bandas/nuevo`)
- ✅ Calendario de fechas (`/fechas`)
- ✅ Publicar fecha con edit token (`/fechas/nueva`)
- ✅ Geolocalización via Nominatim (lat/lng por ciudad)
- ✅ Links de contacto directo (WhatsApp con mensaje pre-llenado, Instagram, Spotify)
- ✅ Sin sistema de autenticación (email/password eliminados)
- ✅ Base de datos en PostgreSQL (Neon.tech)
- ✅ Deploy en Vercel con variables de entorno configuradas
- ✅ Connection pool adaptativo (SQLite local / PostgreSQL remoto según DATABASE_URL)
- ✅ Sistema de "ya vistas" con localStorage
- ✅ Tres temas visuales (claro, oscuro, alto contraste)
- ✅ Perfiles visibles inmediatamente (sin moderación manual)
- ✅ Admin panel presente pero inactivo para aprobaciones
- ✅ Historial de cambios recuperable para writes principales (`/admin/audit`)

## Qué falta para el MVP real

- [ ] **Foto de perfil** — campo + mostrar en grid + detalle + placeholder genérico
- [ ] Buscador/filtros (pospuesto hasta que haya volumen)

## Decisiones vigentes

- Sin autenticación → edit token único por perfil
- Sin chat interno → contacto directo por WhatsApp/Instagram
- Sin sistema de puntuación → descartado para MVP
- Directorio público → cualquiera puede ver sin registrarse
- Buscador removido de landing → agregar cuando haya volumen
- PostgreSQL (Neon.tech) en producción → SQLite para dev local
- Vercel como plataforma de deploy → serverless functions
- Foto de perfil → URL externa opcional, placeholder icono genérico
- Landing grid sin filtros → grid de todos los perfiles
- Moderación desactivada → perfiles, posts y eventos visibles al instante
- Calendario y bandas → adicionales existentes, no core del MVP pero navegables
- Sin dominio propio → `*.vercel.app`
- Auditoría de cambios → snapshots before/after sin `edit_token`

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
- `app/utils.py` — utilidades (coordenadas, distancia, links, tokens)
- `app/templates/` — todos los templates HTML
- `vercel.json` — configuración de deploy
- `api/index.py` — entry point serverless
- `requirements.txt` — dependencias
