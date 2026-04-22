# 2026-04-22 12:31:10 -04:00 — Registro Completo de Modificaciones

## Objetivo del registro

Dejar trazabilidad operativa y tecnica completa del proceso de:

1. Migracion del repositorio a cuenta institucional.
2. Ajustes de versionado para excluir artefactos locales.
3. Preparacion de despliegue en Vercel.
4. Endurecimiento de seguridad del backend Flask.
5. Correccion de bloqueo de despliegue en Vercel y publicacion exitosa.

Este documento queda en ruta versionada (`Registro/`) para continuidad futura del proyecto.

## Estado de repositorios y remotos

- Remoto principal actual:
  - `origin -> https://github.com/DevFisUdeC/CsFisicasWEB_DevFis.git`
- Remoto de respaldo historico:
  - `original -> https://github.com/Nahzap/CsPhysWEB.git`

## Cronologia de commits correlativos

### 1c (`4157a9f`)
- Inicializacion del proyecto en repo.
- Estructura base Flask, templates, estilos, JS, rutas y configuracion inicial.

### 2c (`bbf4215`)
- Gran iteracion funcional:
  - incorporacion de panel admin y modulos asociados,
  - integraciones y ajustes de frontend/backend,
  - actualizaciones de dependencias, estilos, templates y helpers.

### 3c (`2779eb6`)
- Actualizacion de `README.md`.

### 4c (`dbc5e24`)
- Ajustes en templates de contacto/footer/postgrado:
  - `app/templates/components/footer.html`
  - `app/templates/pages/contact.html`
  - `app/templates/pages/graduate.html`

### 5c (`c723012`)
- Eliminacion del control de versiones para material local/no productivo:
  - `Docs/*`
  - `CsFisicasWEB.code-workspace`

### 6c (`b9ed677`)
- Refuerzo de exclusiones en `.gitignore`:
  - `Docs/`
  - `CsFisicasWEB.code-workspace`

### 7c (`097bba6`)
- Preparacion para despliegue en Vercel:
  - `api/index.py` (entrypoint Flask para runtime serverless),
  - `vercel.json` (ruteo y build),
  - `.vercelignore`,
  - actualizacion de `README.md` con pasos de deploy.

### 8c (`d2071b7`)
- Hardening de seguridad:
  - mitigacion de open redirect en login admin (`next` seguro),
  - mitigacion de XSS en `admin.js` (sin `innerHTML` inseguro),
  - configuracion de cookies/sesion por entorno,
  - cabeceras de seguridad HTTP (CSP, HSTS en prod, XFO, XCTO, Referrer-Policy),
  - limites de subida y validacion basica de contenido de imagen,
  - separacion de cliente Supabase `service/public` para reducir privilegio en lecturas publicas,
  - parametrizacion de almacenamiento del rate limiter.

## Eventos operativos relevantes (sin commit de codigo)

1. Se detecto bloqueo inicial en Vercel por autor de commit sin permisos sobre el proyecto.
2. Se instalo y autentico Vercel CLI con cuenta `devfisudec`.
3. Se vinculo el proyecto local al proyecto Vercel institucional:
   - `devfisudecs-projects/cs-fisicas-web-dev-fis`
4. Se realizo despliegue de produccion exitoso.
5. URL de produccion activa:
   - `https://cs-fisicas-web-dev-fis.vercel.app`
6. URL del deployment generado en esa ejecucion:
   - `https://cs-fisicas-web-dev-datnnbkvn-devfisudecs-projects.vercel.app`
7. URL de inspeccion del deployment:
   - `https://vercel.com/devfisudecs-projects/cs-fisicas-web-dev-fis/GRPHCrifdF1gp7ufi7aJNz9ERm1M`

## Ajustes de control de versiones aplicados

- Se mantuvo la decision de no versionar contenido de `Docs/`.
- Se mantuvo la decision de no versionar `CsFisicasWEB.code-workspace`.
- Se agrego exclusion de `.vercel` a `.gitignore` luego del `vercel link`.

## Estado de seguridad actual (resumen de cierre)

- CSRF en formularios admin: activo.
- Login admin protegido por decorador de sesion y rate limit.
- Redirect post-login validado a rutas internas.
- Subida de imagenes con controles adicionales (tipo y tamano).
- Cabeceras de seguridad HTTP en respuestas.
- Separacion de cliente Supabase para lectura publica vs escritura admin.

## Variables de entorno operativas sugeridas (continuidad)

- `SECRET_KEY`
- `ADMIN_USER`
- `ADMIN_PASS_HASH`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SUPABASE_ANON_KEY`
- `SUPABASE_BUCKET`
- `MAX_CONTENT_LENGTH`
- `MAX_UPLOAD_FILE_SIZE`
- `MAX_UPLOAD_FILES`
- `RATELIMIT_STORAGE_URI`

## Riesgos residuales y siguientes pasos recomendados

1. Para entornos institucionales, mover `RATELIMIT_STORAGE_URI` a backend persistente (Redis) y evitar `memory://`.
2. Consolidar politicas RLS en Supabase para lectura publica y escritura restringida al backend admin.
3. Definir pipeline de respaldo y restauracion de datos (DB y storage).
4. Incorporar pruebas automatizadas de rutas admin criticas (login, CRUD, upload).
5. Mantener registro operativo en esta carpeta con prefijo `YYYY-MM-DD_HH-mm-ss_`.

## Convencion acordada para futuros registros

- Formato de archivo:
  - `Registro/YYYY-MM-DD_HH-mm-ss_NOMBRE.md`
- Regla de contenido:
  - iniciar siempre con fecha y hora exacta al principio,
  - luego nombre del registro,
  - incluir objetivo, cambios, comandos relevantes, estado final y pendientes.
