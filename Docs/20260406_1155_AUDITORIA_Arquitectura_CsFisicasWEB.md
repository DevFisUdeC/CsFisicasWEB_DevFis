# Auditoría de Arquitectura — CsFisicasWEB
**Fecha:** 06 de abril de 2026, 11:55  
**Proyecto:** Sitio web del Departamento de Física — Universidad de Concepción  
**URL objetivo:** https://fisica.udec.cl  
**Revisado por:** Agente de arquitectura (Cursor AI)

---

## Índice

1. [Contexto del proyecto](#1-contexto-del-proyecto)
2. [Stack tecnológico](#2-stack-tecnológico)
3. [Arquitectura general](#3-arquitectura-general)
4. [Inventario de rutas](#4-inventario-de-rutas)
5. [Análisis del backend](#5-análisis-del-backend)
6. [Análisis del frontend](#6-análisis-del-frontend)
7. [Panel de administración](#7-panel-de-administración)
8. [Bugs y errores concretos](#8-bugs-y-errores-concretos)
9. [Mejoras priorizadas](#9-mejoras-priorizadas)
10. [Estado de la documentación interna](#10-estado-de-la-documentación-interna)

---

## 1. Contexto del proyecto

**CsFisicasWEB** es un sitio web institucional para el Departamento de Ciencias Físicas de la Universidad de Concepción. Su propósito es:

- Difundir la oferta académica (pregrado y postgrado)
- Presentar al equipo docente y sus líneas de investigación
- Publicar noticias y novedades del departamento
- Proveer un panel CMS interno para gestión de contenido

El sitio está en construcción activa. Al momento de esta auditoría, las funcionalidades principales están implementadas pero se identificaron defectos de calidad, inconsistencias y riesgos de seguridad que deben atenderse antes de un despliegue en producción.

---

## 2. Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Python + Flask | 3.1 |
| Templates | Jinja2 | (bundled con Flask) |
| Base de datos | Supabase (PostgreSQL) | supabase-py 2.28.x |
| Almacenamiento | Supabase Storage | — |
| Datos estáticos | JSON en disco | — |
| Frontend CSS | CSS vanilla + design tokens | — |
| Frontend JS | JavaScript vanilla | — |
| Configuración | python-dotenv | — |
| Deploy target | Vercel | — |
| Control de versiones | Git | — |

**Sin frameworks de frontend** (no React, Vue, ni similar). El sitio es renderizado completamente en servidor (SSR) con Jinja2.

---

## 3. Arquitectura general

### Diagrama de flujo

```
┌──────────────────────────────────────────────────────────┐
│                     Cliente / Browser                     │
└───────────────────────────┬──────────────────────────────┘
                            │ HTTP Request
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    Flask Application                      │
│                                                           │
│  create_app()  ←── config.py (.env)                       │
│       │                                                   │
│       ├── main_bp        /                                │
│       ├── academics_bp   /academics                       │
│       ├── research_bp    /research                        │
│       ├── people_bp      /people                          │
│       ├── news_bp        /news                            │
│       └── admin_bp       /admin  ←── auth.py              │
│                                                           │
│  helpers.py  ──── Supabase CRUD (news, team_members)      │
│  helpers.py  ──── JSON cache (programs, research)         │
│  _get_nav_items()  ──── context_processor global          │
│  navigation.py     ──── ⚠ NO CONECTADO                    │
└─────────────────────┬───────────────┬────────────────────┘
                      │               │
          ┌───────────▼───┐   ┌───────▼────────┐
          │   Supabase    │   │   JSON files   │
          │  PostgreSQL   │   │  (en disco,    │
          │  + Storage    │   │  cache en mem) │
          └───────────────┘   └────────────────┘
```

### Estructura de archivos relevantes

```
app/
├── __init__.py          ← Application factory + context processors
├── auth.py              ← Decorador login_required
├── database.py          ← Singleton cliente Supabase
├── helpers.py           ← CRUD Supabase + loaders JSON + slugify
├── navigation.py        ← ⚠ Duplicado de nav, no importado
├── data/
│   ├── programs.json    ← Datos de pregrado/postgrado
│   └── research.json    ← Líneas de investigación
├── routes/
│   ├── main.py          ← Blueprint: home, about, contact
│   ├── academics.py     ← Blueprint: undergraduate, graduate
│   ├── research.py      ← Blueprint: index, publications, labs
│   ├── people.py        ← Blueprint: index, detail (slug)
│   ├── news.py          ← Blueprint: index, detail (slug)
│   └── admin.py         ← Blueprint: login/logout + CRUD CMS
├── templates/
│   ├── base.html        ← Layout público raíz
│   ├── pages/           ← Páginas públicas
│   ├── components/      ← Navbar, footer, hero, cards
│   └── admin/           ← Panel de administración
└── static/
    ├── css/             ← design-system, layout, components, admin
    └── js/              ← main.js, navigation.js, admin.js
```

---

## 4. Inventario de rutas

### Rutas públicas

| Método | URL | Handler | Fuente de datos |
|--------|-----|---------|----------------|
| GET | `/` | `main.home` | Supabase (noticias) |
| GET | `/about` | `main.about` | — (estática) |
| GET | `/contact` | `main.contact` | — (estática) |
| GET | `/academics/undergraduate` | `academics.undergraduate` | `programs.json` |
| GET | `/academics/graduate` | `academics.graduate` | `programs.json` |
| GET | `/research/` | `research.index` | `research.json` |
| GET | `/research/publications` | `research.publications` | — (estática) |
| GET | `/research/labs` | `research.labs` | — (estática) |
| GET | `/people/` | `people.index` | Supabase |
| GET | `/people/<slug>` | `people.detail` | Supabase (full scan) |
| GET | `/news/` | `news.index` | Supabase |
| GET | `/news/<slug>` | `news.detail` | Supabase (full scan) |

### Rutas de administración (requieren sesión)

| Método | URL | Handler |
|--------|-----|---------|
| GET/POST | `/admin/login` | `admin.login` |
| GET | `/admin/logout` | `admin.logout` |
| GET | `/admin/` | `admin.dashboard` |
| GET | `/admin/news` | `admin.news_list` |
| GET/POST | `/admin/news/create` | `admin.create_news_view` |
| GET/POST | `/admin/news/edit/<slug>` | `admin.edit_news_view` |
| POST | `/admin/news/delete/<slug>` | `admin.delete_news_view` |
| GET | `/admin/team` | `admin.team_list` |
| GET/POST | `/admin/team/create` | `admin.create_member` |
| GET/POST | `/admin/team/edit/<slug>` | `admin.edit_member` |
| POST | `/admin/team/delete/<slug>` | `admin.delete_member` |
| GET | `/admin/images` | `admin.image_gallery` |
| POST | `/admin/images/upload` | `admin.upload_image` |
| POST | `/admin/images/delete` | `admin.delete_image` |

### Ruta fantasma (404 garantizado)

| URL | Referencia | Estado |
|-----|-----------|--------|
| `/academics/curriculum` | `_get_nav_items()` en `__init__.py` | **Sin ruta registrada** |

---

## 5. Análisis del backend

### 5.1 Application Factory (`app/__init__.py`)

- Bien estructurado con `create_app(config_name)` y soporte multi-entorno.
- Los `context_processors` inyectan `site_config` y `nav_items` globalmente — correcto.
- **Problema:** Define `_get_nav_items()` internamente en lugar de importar `navigation.py`. Ambos coexisten con diferencias sutiles, creando una fuente de verdad duplicada.

### 5.2 Configuración (`config.py`)

- Jerarquía `Config → DevelopmentConfig / ProductionConfig / TestingConfig` — buena práctica.
- `SECRET_KEY` tiene un valor hardcoded de fallback `"dev-key-change-in-production"`.
- `ADMIN_USER` / `ADMIN_PASS` tienen defaults `"admin"` / `"admin"` — **crítico para producción**.
- `ALLOWED_EXTENSIONS` **no está definido** en la clase `Config`; `admin.py` lo recupera con `current_app.config.get('ALLOWED_EXTENSIONS', {...})` usando un fallback inline.

### 5.3 Capa de datos (`helpers.py` + `database.py`)

- `database.py` implementa un singleton limpio para el cliente Supabase.
- `helpers.py` centraliza todo el acceso a datos (CRUD + JSON) — buen principio SRP desde la perspectiva de los blueprints.
- **Cache de JSON:** `_cache` en módulo, sin TTL ni invalidación. Aceptable para datos que cambian raramente, pero requiere restart para reflejar cambios en disco.
- **`load_json` silencia errores:** Retorna `[]` si el archivo no existe o tiene JSON inválido. `get_programs()` luego llama `.get()` sobre ese resultado, lo que generaría `AttributeError` si el archivo falla.
- **`slugify` limitado:** Solo maneja caracteres ASCII. Nombres con tildes o ñ producen slugs incorrectos (ej: `"Ángel"` → `"-ngel"`).
- **`get_news_by_slug` existe pero no se usa** en la ruta pública `news.detail`.
- **`get_member_by_slug` existe pero no se usa** en la ruta pública `people.detail`.

### 5.4 Autenticación (`auth.py`)

- Basada en `session['logged_in']` — funcional para un CMS pequeño.
- Sin hash de contraseña (comparación de string plano contra `.env`).
- Sin protección CSRF en formularios de admin.
- Sin rate limiting en `/admin/login`.
- Sin expiración de sesión configurable.

---

## 6. Análisis del frontend

### 6.1 Sistema de templates

La herencia es limpia y consistente:

```
base.html
└── pages/*.html (home, about, contact, news, research, people, etc.)
    └── components/ (navbar, footer, hero, cards) [includes]

admin/base.html
└── admin/*.html (dashboard, news, team, images, forms)

admin/login.html  ← standalone, sin extends
```

Bloques disponibles en `base.html`: `title`, `meta_description`, `content`, `extra_css`, `extra_js`.

### 6.2 Design System (CSS)

El sistema de diseño está bien organizado en tres capas:

| Archivo | Responsabilidad |
|---------|----------------|
| `design-system.css` | Tokens CSS (colores, tipografía, espaciado), reset, utilidades |
| `layout.css` | Contenedores, grids, secciones, breakpoints |
| `components.css` | Todos los componentes UI: navbar, hero, cards, botones, badges, etc. |
| `admin.css` | Layout y componentes específicos del panel admin |

**Paleta:** Tema oscuro con azules UdeC (`#0D1117` base) y dorado como color de acción primaria.

**Breakpoints:**
- `1080px` — Navbar: menú de escritorio → hamburger
- `768px` — Grids a una columna, layouts de dos columnas apilados
- `600px` — Ajustes secundarios (logo navbar oculto, admin sidebar colapsado)
- `480px` — Padding reducido, tipografía más pequeña

### 6.3 JavaScript

| Archivo | Función |
|---------|---------|
| `navigation.js` | Toggle menú móvil con `aria-expanded`, cierre con Escape/click externo |
| `main.js` | Destacar enlace activo en navbar por coincidencia de pathname |
| `admin.js` | Preview de imagen, tag input, confirmación de borrado, copia de URL al portapapeles, auto-hide de toasts |

### 6.4 Accesibilidad

- Skip link implementado en `base.html` ✓
- `aria-expanded` en menú móvil ✓
- `aria-labelledby` en secciones ✓
- Focus states en `design-system.css` ✓
- Falta: soporte de teclado para dropdowns del navbar (solo funcionan con `:hover` en escritorio)

---

## 7. Panel de administración

Estructura completa y funcional:

- **Login** standalone (sin heredar del base admin)
- **Dashboard** con contadores (noticias, académicos, imágenes)
- **Noticias:** CRUD completo con upload de imagen portada
- **Académicos:** CRUD completo con tag input para áreas de investigación
- **Imágenes:** Galería con upload múltiple, copia de URL pública, borrado

El admin usa las mismas tablas Supabase que el sitio público, por lo que los cambios son inmediatos.

---

## 8. Bugs y errores concretos

### CRÍTICOS — Funcionalidad rota

| # | Descripción | Archivo | Impacto |
|---|-------------|---------|---------|
| B01 | URL `/academics/curriculum` en navbar apunta a una ruta inexistente | `app/__init__.py`, `_get_nav_items()` | 404 en producción al hacer click |
| B02 | Tabla HTML con `<td>` sin `<tr>` envolvente | `app/templates/pages/undergraduate.html` ~líneas 218–230 | Tabla de aranceles renderiza incorrectamente |
| B03 | `people.detail` y `news.detail` cargan todas las filas y filtran en Python | `app/routes/people.py`, `app/routes/news.py` | Ineficiencia; helpers con query por slug ya existen sin usar |

### ALTAS — Seguridad

| # | Descripción | Archivo | Impacto |
|---|-------------|---------|---------|
| S01 | Sin CSRF tokens en formularios del admin | `app/templates/admin/*.html` | Vulnerable a CSRF attacks |
| S02 | Contraseña admin comparada en texto plano | `app/routes/admin.py`, `config.py` | Sin protección si `.env` se expone |
| S03 | Sin rate limiting en `/admin/login` | `app/routes/admin.py` | Vulnerable a fuerza bruta |
| S04 | `ALLOWED_EXTENSIONS` no en `Config` | `config.py`, `app/routes/admin.py` | Configuración de extensiones inconsistente |

### MEDIAS — Calidad de código y UI

| # | Descripción | Archivo | Impacto |
|---|-------------|---------|---------|
| M01 | `--shadow-xl` usado pero no definido | `app/static/css/components.css` | Hover sin sombra en curriculum e imagen welcome |
| M02 | `.badge--sm` usado pero no definido | `app/static/css/components.css`, `app/templates/pages/research.html` | Keywords de investigación sin tamaño correcto |
| M03 | `.navbar__toggle.is-active` sin estilos CSS | `app/static/js/navigation.js`, `app/static/css/components.css` | Animación de hamburger no visible |
| M04 | Iconos de `graduate.html` vacíos | `app/templates/pages/graduate.html` | `<span>` vacíos en tarjetas de programas |
| M05 | Dos sistemas de toast paralelos | `components.css` (`.toast`), `admin.css` (`.admin-toast`) | Mantenimiento duplicado |
| M06 | `login.html` con `<style>` inline | `app/templates/admin/login.html` | Diverge del design system, difícil mantener |
| M07 | `navigation.py` definido pero no importado | `app/navigation.py` | Código muerto con diferencias vs `__init__.py` |

### BAJAS — Mejoras futuras

| # | Descripción | Impacto |
|---|-------------|---------|
| L01 | `slugify` sin soporte de tildes/ñ | Slugs malformados para nombres españoles |
| L02 | Cache JSON sin TTL ni invalidación | Requiere restart para reflejar cambios en disco |
| L03 | `load_json` retorna `[]` silenciosamente ante errores | `get_programs()` podría lanzar `AttributeError` |
| L04 | Preview de imagen sólo para `files[0]` en upload múltiple | UX incompleta en galería de imágenes |
| L05 | README vacío, Docs sin documentación escrita | Sin guía de setup ni onboarding |
| L06 | `meta_description` no especificado por página | SEO básico sin implementar |
| L07 | Dropdowns del navbar sin soporte de teclado | Accesibilidad limitada para usuarios de teclado |

---

## 9. Mejoras priorizadas

### Roadmap sugerido por fase

#### Fase 1 — Bugs críticos (antes de ir a producción)

- [ ] **B01** Corregir URL de "Malla Curricular" en `_get_nav_items()` o crear la ruta faltante
- [ ] **B02** Corregir estructura HTML de tabla de aranceles en `undergraduate.html`
- [ ] **B03** Usar `get_member_by_slug()` y `get_news_by_slug()` en rutas de detalle públicas

#### Fase 2 — Seguridad (antes de ir a producción)

- [ ] **S01** Agregar Flask-WTF o tokens CSRF manuales a formularios del admin
- [ ] **S02** Hashear contraseña del admin con `bcrypt` o `werkzeug.security`
- [ ] **S03** Agregar rate limiting con `Flask-Limiter` en `/admin/login`
- [ ] **S04** Mover `ALLOWED_EXTENSIONS` a `Config` en `config.py`

#### Fase 3 — Calidad de código (sprint siguiente)

- [ ] **M01** Agregar `--shadow-xl` a `design-system.css`
- [ ] **M02** Agregar `.badge--sm` a `components.css`
- [ ] **M03** Agregar estilos para `.navbar__toggle.is-active` (animación hamburger)
- [ ] **M04** Corregir lógica de iconos en `graduate.html`
- [ ] **M05** Unificar sistemas de toast en un único componente
- [ ] **M06** Mover estilos de `login.html` a `admin.css`
- [ ] **M07** Decidir: usar `navigation.py` e importarlo, o eliminarlo

#### Fase 4 — Mejoras UX/DX (backlog)

- [ ] **L01** Mejorar `slugify` con `unicodedata.normalize` para tildes y ñ
- [ ] **L02** Agregar endpoint `/admin/reload-cache` para invalidar JSON sin restart
- [ ] **L03** Manejo de errores explícito en `load_json` (raise en vez de silenciar)
- [ ] **L04** Mejorar preview de imágenes para upload múltiple en `admin.js`
- [ ] **L05** Escribir README con instrucciones de setup y despliegue
- [ ] **L06** Agregar `meta_description` específico en cada template de página
- [ ] **L07** Implementar manejo de teclado para dropdowns del navbar

---

## 10. Estado de la documentación interna

| Item | Estado |
|------|--------|
| `README.md` | Vacío |
| `Docs/` | Solo contiene logos SVG de UdeC, sin markdown |
| `.env` | Presente (no versionado, correcto) |
| `requirements.txt` | Al día con dependencias actuales |
| Comentarios en código | Escasos pero presentes en los archivos principales |

**Recomendación:** Completar `README.md` con instrucciones de instalación local, variables de entorno requeridas y estructura del proyecto. Esto es necesario para cualquier colaborador nuevo o para el proceso de deploy.

---

*Documento generado el 06/04/2026 a las 11:55 — Revisión inicial de arquitectura.*  
*Próxima revisión recomendada: tras completar Fase 1 y Fase 2.*
