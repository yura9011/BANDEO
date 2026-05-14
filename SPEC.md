# SPEC — BANDEO

> Estado: `FINALIZED`

## Qué es

Directorio público de músicos y bandas. La gente entra, ve perfiles, y contacta directo por WhatsApp o Instagram. Sin registro, sin fricción.

## Qué no es

- No es una red social (no hay feed, no hay follows, no hay likes)
- No tiene chat interno (el contacto es externo)
- No almacena archivos multimedia (links a YouTube/Spotify/Instagram, foto por URL externa)
- No tiene sistema de puntuación en el MVP

---

## Flujos principales

### Buscar un músico
1. Entrar a `/`
2. Ver el grid de perfiles
3. Click en un perfil
4. Ver detalle con bio, videos y links
5. Click en "Contactar por WhatsApp" o Instagram/Spotify

### Publicar un perfil
1. Ir a `/create`
2. Llenar el formulario (nombre, rol, ciudad, instrumentos, géneros, bio, foto URL, links)
3. Guardar el edit link que aparece
4. El perfil queda visible inmediatamente en el directorio

### Editar un perfil
1. Usar el edit link guardado: `/edit/{token}`
2. Modificar y guardar

### Publicar una novedad (bandas)
1. Ir a `/bandas/nuevo`
2. Ingresar el edit token
3. Escribir la novedad (máx 500 chars)
4. Aparece en `/bandas`

### Publicar una fecha
1. Ir a `/fechas/nueva`
2. Ingresar el edit token
3. Completar fecha, venue, ciudad
4. Aparece en el calendario de `/fechas`

---

## Modelos de datos

### User
- `id`, `display_name`, `role` (MUSICO / BANDA)
- `edit_token` — token único para editar
- `status` — default `approved` (sin moderación en MVP)
- `created_at`

### Profile
- `user_id`, `city`, `lat`, `lng`
- `instruments`, `genres` — strings separados por coma, lowercase
- `bio`, `phone`, `youtube_links`, `spotify_link`, `instagram_link`
- `photo_url` — URL externa opcional

### Post
- `user_id`, `content` (máx 500 chars), `created_at`

### Event
- `user_id`, `band_name`, `date`, `time`, `venue`, `address`, `city`, `price`, `details`

---

## Stack

- **Backend:** Python 3.10+, FastAPI, SQLModel, Uvicorn
- **Base de datos:** PostgreSQL (Neon.tech) en prod, SQLite en dev local
- **Frontend:** Jinja2 templates, Tailwind CSS (CDN)
- **Geocoding:** Nominatim (OpenStreetMap), sin API key
- **Deploy:** Vercel (serverless)
- **Storage:** Ninguno — foto vía URL externa, videos vía YouTube/Spotify embebido

---

## Criterios de éxito del MVP

- [ ] Alguien puede publicar su perfil en menos de 3 minutos
- [ ] Alguien puede encontrar un músico y contactarlo por WhatsApp
- [ ] Funciona en celular
- [ ] Está deployado y accesible públicamente
- [ ] Los perfiles tienen foto (o placeholder genérico)

---

## Reglas de desarrollo

### Cambios de schema
Antes de agregar cualquier campo nuevo a un modelo:
1. Verificar si la tabla ya existe en Neon
2. Si existe, crear ruta `/admin/migrate` con `ALTER TABLE` explícito o ejecutar directo en dashboard de Neon
3. Deployar la migración primero, verificar que funciona
4. Recién después deployar el código que usa el campo nuevo

### Cambios de dependencias
Antes de agregar un nuevo driver o librería:
1. Verificar que esté disponible en el entorno de Vercel
2. Testear localmente con `pip install` limpio
3. Documentar en STATE.md si hay restricciones

### Credenciales
- Nunca en el código
- Nunca en el repo
- Solo en Vercel dashboard y en .env local (ignorado por git)

---

## Licencia y dominio

- Sin dominio propio por ahora — deployado en `*.vercel.app`
- Licencia MIT
