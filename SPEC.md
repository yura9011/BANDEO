# SPEC — BANDEO

> Estado: `EN DESARROLLO`

## Qué es

Directorio público de músicos y bandas. La gente entra, ve perfiles, y contacta directo por WhatsApp o Instagram. Sin registro, sin fricción.

## Qué no es

- No es una red social (no hay feed, no hay follows, no hay likes)
- No tiene chat interno (el contacto es externo)
- No almacena archivos multimedia (links a YouTube/Spotify/Instagram)
- No tiene sistema de puntuación en el MVP

---

## Flujos principales

### Buscar un músico
1. Entrar a `/`
2. Ver el grid de perfiles
3. Click en un perfil
4. Click en "Contactar por WhatsApp"

### Publicar un perfil
1. Ir a `/create`
2. Llenar el formulario
3. Guardar el edit link que aparece
4. El perfil queda visible en el directorio

### Editar un perfil
1. Usar el edit link guardado: `/edit/{token}`
2. Modificar y guardar

### Publicar una novedad (bandas)
1. Ir a `/bandas/nuevo`
2. Ingresar el edit token
3. Escribir la novedad (máx 500 chars)
4. Aparece en `/bandas`

---

## Modelos de datos

### User
- `id`, `display_name`, `role` (MUSICO / BANDA)
- `edit_token` — token único para editar
- `created_at`

### Profile
- `user_id`, `city`, `lat`, `lng`
- `instruments`, `genres` — strings separados por coma, lowercase
- `bio`, `phone`, `youtube_links`, `spotify_link`, `instagram_link`

### Post
- `user_id`, `content` (máx 500 chars), `created_at`

---

## Stack

Ver `.gsd/STACK.md`

---

## Criterios de éxito del MVP

- [ ] Alguien puede publicar su perfil en menos de 3 minutos
- [ ] Alguien puede encontrar un músico y contactarlo por WhatsApp
- [ ] Funciona en celular
- [ ] Está deployado y accesible públicamente
