# CsFisicasWEB — README de desarrollo personal

Este documento es para uso personal de desarrollo y seguimiento del proyecto.
No está orientado a documentación pública ni onboarding externo.

## Estado actual del proyecto

Sitio web del Departamento de Física (UdeC) con:

- Backend en Flask (SSR con Jinja2)
- Datos dinámicos en Supabase (noticias, académicos, imágenes)
- Datos estáticos en JSON (`programs.json`, `research.json`)
- Panel admin para CRUD de contenidos
- Frontend en CSS/JS vanilla con design system propio

## Cambios ya implementados (última ronda)

### Correcciones críticas
- Corregido enlace roto de Malla Curricular en navegación.
- Corregida estructura HTML inválida en tabla de aranceles de pregrado.
- Optimizadas rutas de detalle (`people/<slug>`, `news/<slug>`) para consultar por slug directo en Supabase.

### Seguridad
- CSRF habilitado con `Flask-WTF` en formularios de admin (incluyendo login y delete forms).
- Login admin preparado para hash de contraseña (`ADMIN_PASS_HASH`) con fallback dev.
- Rate limiting aplicado a login admin (`10/minute`).
- `ALLOWED_EXTENSIONS` movido a `Config`.

### UI y mantenibilidad
- Agregado token de sombra `--shadow-xl`.
- Agregada clase `.badge--sm`.
- Agregada animación visual para botón hamburguesa activo.
- Corregidos iconos vacíos en vista de postgrado.
- Estilos inline de `admin/login.html` movidos a `admin.css`.
- Eliminado `app/navigation.py` duplicado (se mantiene fuente de verdad en `app/__init__.py`).

### DX / calidad de datos
- `slugify()` mejorado para soportar tildes/ñ (normalización unicode).
- `load_json()` endurecido para evitar errores por tipo inesperado.
- Preview de imágenes en admin mejorado para selección múltiple.

## Arquitectura resumida

### Flujo general
1. `run.py` inicia app Flask con `create_app('development')`.
2. `app/__init__.py`:
   - carga config
   - inicializa Supabase + CSRF + limiter
   - registra blueprints
   - inyecta contexto global de sitio
3. Blueprints renderizan templates Jinja y consumen helpers.
4. Helpers consumen Supabase (DB y Storage) o JSON local.

### Blueprints
- `main` → home / about / contact
- `academics` → pregrado / postgrado
- `research` → líneas / publicaciones / labs
- `people` → listado y detalle académicos
- `news` → listado y detalle noticias
- `admin` → login + dashboard + CRUD + galería

## Estructura principal

```
app/
  __init__.py
  auth.py
  database.py
  helpers.py
  routes/
  templates/
  static/
  data/
config.py
run.py
requirements.txt
Docs/
```

## Variables de entorno mínimas

Archivo `.env` (local):

- `SECRET_KEY`
- `ADMIN_USER`
- `ADMIN_PASS` (solo dev) o `ADMIN_PASS_HASH` (recomendado)
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SUPABASE_BUCKET` (opcional, default: `uploads`)
- `APP_ENV` (`development` o `production`)
- `LOG_LEVEL` (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `FLASK_DEBUG` (`true`/`false`, opcional para sobreescribir debug)

## Ejecución local

1. Crear/activar entorno virtual.
2. Instalar dependencias:
   - `pip install -r requirements.txt`
3. Ejecutar:
   - `python run.py`
4. Abrir:
   - `http://127.0.0.1:5000`

### Modo debug (logs detallados en terminal)

PowerShell:

- `$env:APP_ENV="development"`
- `$env:LOG_LEVEL="DEBUG"`
- `$env:FLASK_DEBUG="true"`
- `python run.py`

Con esta configuración se habilita:

- Trazabilidad por request (`REQUEST START/END`)
- Trazabilidad por función backend (`ENTER/EXIT/ERROR`) en rutas/helpers/auth/database
- Trazabilidad frontend en consola del navegador (`window.appLog`) para:
  - carga de página,
  - clicks de navegación y botones,
  - toggle/cierre de menú móvil,
  - carga de iframes (ej. mapas),
  - errores de carga de imágenes.

### Modo producción local (logs acotados)

PowerShell:

- `$env:APP_ENV="production"`
- `$env:LOG_LEVEL="WARNING"`
- `$env:FLASK_DEBUG="false"`
- `python run.py`

## Despliegue en Vercel

El proyecto ya incluye configuración para Vercel:

- `api/index.py` como entrypoint serverless Flask en modo `production`.
- `vercel.json` para enrutar todo el tráfico hacia la app Flask.

Pasos para desplegar:

1. Importar el repositorio `DevFisUdeC/CsFisicasWEB_DevFis` en Vercel.
2. En `Project Settings > Environment Variables`, definir:
   - `SECRET_KEY`
   - `ADMIN_USER`
   - `ADMIN_PASS_HASH` (recomendado en producción)
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `SUPABASE_BUCKET` (opcional)
3. Ejecutar deploy (Production).

Nota: si faltan `SUPABASE_URL` o `SUPABASE_SERVICE_KEY`, la app fallará al iniciar por diseño de seguridad.

## Dependencias principales

- `flask==3.1.0`
- `flask-wtf==1.2.2`
- `flask-limiter==3.12`
- `python-dotenv==1.1.0`
- `supabase==2.28.3`

## Checklist de continuidad (próximo desarrollo)

- [ ] Definir estrategia final de autenticación admin (solo hash o migrar a auth externo)
- [ ] Revisar semántica y accesibilidad de dropdowns por teclado en navbar
- [ ] Consolidar completamente sistema de toasts (public/admin) si se busca un solo componente real
- [ ] Completar SEO básico por página (`meta_description`)
- [ ] Agregar tests mínimos para rutas críticas y login

## Síntesis final

Actualmente, CsFisicasWEB funciona como un CMS institucional en Flask con Supabase, con base técnica estable para seguir iterando contenido, diseño y seguridad. La app ya tiene rutas públicas/admin operativas, hardening inicial aplicado (CSRF + rate limit + password hash support) y mejoras de calidad en frontend/backend que corrigen los puntos críticos detectados en auditoría.
