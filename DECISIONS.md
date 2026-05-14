# DECISIONS.md — Architecture Decision Records

> **Proposito**: Registrar decisiones tecnicas y de diseno significativas.

---

## [DECISION-001] Sin autenticacion: edit tokens

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
El registro de usuarios agregaba friccion innecesaria. La gente quiere buscar musicos y contactarlos, no crear cuentas.

### Decision
Eliminar registro/login/passwords. Cada perfil tiene un `edit_token` (UUID) que permite editar sin autenticacion.

### Consecuencias
- No hay proteccion contra spam (futuro: rate limiting por IP)
- Si el usuario pierde el token, no puede editar (futuro: recuperacion por email opcional)
- Flujo de creacion drasticamente mas simple

---

## [DECISION-002] Sin chat interno

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
Implementar chat interno requiere backend de mensajeria en tiempo real, almacenamiento de mensajes, notificaciones.

### Decision
Redirigir todo contacto a plataformas externas: WhatsApp (link directo con mensaje pre-llenado), Instagram, Spotify.

### Consecuencias
- No necesitamos backend de chat
- La conversacion queda fuera de BANDEO
- El usuario necesita tener WhatsApp/Instagram instalado

---

## [DECISION-003] Sin sistema de puntuacion

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
MVP debe ser minimo. Ratings agregan complejidad (moderacion, fake reviews, calculo de score).

### Decision
Descartar ratings para MVP.

---

## [DECISION-004] Directorio publico sin buscador

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
Sin volumen de perfiles, un buscador esta vacio y no tiene sentido.

### Decision
Landing muestra grid de todos los perfiles. Buscador/filtros se agregan cuando haya volumen suficiente.

---

## [DECISION-005] Foto de perfil via URL externa

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
Necesitamos fotos de perfil pero no queremos storage propio ni costos adicionales.

### Decision
Campo `photo_url` opcional. El usuario pega una URL externa. Placeholder: icono generico (silueta) si no hay foto.

### Alternativas consideradas
- Subida a VPS propio: requiere infraestructura adicional
- Vercel Blob: requiere plan pago
- URL externa: mas simple, sin storage

---

## [DECISION-006] Sin moderacion: perfiles visibles inmediatamente

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
El flujo de pending->approved agregaba friccion: el usuario crea un perfil y no aparece hasta que el admin lo aprueba.

### Decision
Default `status = "approved"` para User, Post, Event. Admin panel se conserva pero no se usa activamente.

### Consecuencias
- Riesgo de spam (mitigacion futura: moderacion manual si es necesario)
- Experiencia inmediata para el usuario

---

## [DECISION-007] Deploy en Vercel + Neon PostgreSQL

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
Necesitamos un deploy serverless gratuito con base de datos PostgreSQL.

### Decision
Vercel para serverless functions, Neon.tech para PostgreSQL. Driver psycopg2 con SSL requerido. SQLite para desarrollo local.

---

## [DECISION-008] Sin dominio propio

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
Comprar un dominio tiene costo y configuracion adicional.

### Decision
Usar `*.vercel.app` por ahora. Dominio propio cuando haya presupuesto.

---

## [DECISION-009] Calendario y bandas como adicionales

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
El codigo actual incluye `/bandas` (novedades) y `/fechas` (calendario). No estaban en el spec original pero ya estan implementados.

### Decision
Mantenerlos navegables desde el header pero no promocionarlos activamente. No son core del MVP.

---

## [DECISION-010] Diseno de foto en grid y detalle

**Fecha**: 2026-05-14
**Estado**: Accepted

### Contexto
Definir como se muestra la foto en el grid de perfiles y en el detalle.

### Decision
- Grid: foto circular arriba a la izquierda del card. Placeholder: icono generico de persona.
- Detalle: foto grande centrada arriba del bio.
- Formularios: campo `photo_url` al final, despues de bio, antes de links.

---

*Ultima actualizacion: 2026-05-14*
