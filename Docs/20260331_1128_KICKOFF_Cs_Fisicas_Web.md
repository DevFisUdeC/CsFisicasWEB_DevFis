# 📋 KICKOFF — Proyecto CsFisicasWEB

> **Fecha:** 31 de marzo de 2026 · 11:28 hrs (CLT, UTC-3)  
> **Proyecto:** Rediseño web del Departamento de Física — Universidad de Concepción  
> **Objetivo:** Reemplazar [fisica.udec.cl](https://fisica.udec.cl/) con una aplicación Flask elegante y académica  
> **Stack:** Python Flask + Jinja2 + Vanilla CSS + JavaScript  

---

## 1. Diagnóstico del Sitio Actual (`fisica.udec.cl`)

### Estado Actual — WordPress/Kubio

| Aspecto | Evaluación | Detalle |
|---|---|---|
| **Contenido** | ⚠️ Mínimo | Solo un hero section con eslogan y dos botones genéricos |
| **Navegación** | ❌ Inexistente | Sin menú, sin páginas internas, sin estructura informativa |
| **Diseño visual** | ❌ Genérico | Template WordPress sin identidad departamental |
| **Rendimiento** | ❌ Deficiente | Carga pesada por WordPress + plugins innecesarios |
| **Accesibilidad** | ❌ No cumple | Sin skip links, sin ARIA, sin estructura semántica |
| **Mobile** | ⚠️ Básico | Responsive genérico del template, no optimizado |
| **SEO** | ❌ Nulo | Sin meta descriptions, sin estructura H1-H6 adecuada |
| **Información académica** | ❌ Ausente | No hay info de carreras, investigación, académicos |

### Contenido Actual Extraído

El sitio actual contiene únicamente:
- Un título: *"Departamento de Física"*
- Un párrafo descriptivo genérico
- Dos botones: "Conócenos" y "Contáctanos" (ambos enlazan a la misma página)
- Un footer con copyright y créditos de Kubio

**Conclusión:** El sitio actual no cumple ningún estándar de calidad web y no ofrece valor informativo al usuario.

---

## 2. Análisis de Sitios de Referencia

### 2.1 — [cfm.cl](https://www.cfm.cl/) (Facultad de Ciencias Físicas y Matemáticas)

| Aspecto | Observación | Adopción |
|---|---|---|
| **Navegación** | Mega-menú con 7+ secciones principales, submenús anidados | ✅ Adaptar estructura jerárquica para Departamento de Física |
| **Contenido** | Noticias con thumbnails, carreras, postgrado, departamentos | ✅ Implementar feed de noticias dinámico |
| **Redes sociales** | YouTube, Facebook, Twitter, Instagram en header | ✅ Incluir redes sociales del departamento |
| **Estructura** | Secciones: Facultad, Pregrado, Departamentos, Investigación, Carreras, Postgrado, Servicios | ✅ Mapear a las secciones del departamento |
| **Diseño** | Formal pero algo anticuado (ThemeIsle/WordPress) | ⚠️ Mejorar significativamente la estética |

**Fortalezas a emular:** Estructura de navegación completa, cobertura informativa amplia, integración de noticias.  
**Debilidades a mejorar:** Diseño visual datado, navegación redundante, carga lenta por WordPress.

### 2.2 — [fi.udec.cl](https://fi.udec.cl/) (Facultad de Ingeniería)

| Aspecto | Observación | Adopción |
|---|---|---|
| **Hero section** | Carrusel con mensaje de innovación y CTA | ✅ Implementar hero dinámico con partículas/animación |
| **Cifras** | Estadísticas de alumnos, empleabilidad, convenios | ✅ Sección de cifras clave del departamento |
| **Noticias** | Grid de cards con imagen, autor, fecha, categoría | ✅ Grid de noticias con filtrado por categoría |
| **Agenda** | Sección dedicada a eventos y actividades | ✅ Calendario de seminarios y eventos |
| **Accesibilidad** | Toolbar WP Accessibility con contraste, tamaño, etc. | ✅ Implementar controles de accesibilidad nativos |
| **Carreras** | Listado extenso con enlaces individuales | ✅ Página dedicada a Cs. Físicas con info detallada |

**Fortalezas a emular:** Sección de cifras, diseño moderno del grid de noticias, toolbar de accesibilidad.  
**Debilidades a mejorar:** Duplicación de elementos de navegación, rendimiento general.

### 2.3 — [udec.cl](https://www.udec.cl/) (Universidad de Concepción)

| Aspecto | Observación | Adopción |
|---|---|---|
| **Identidad** | Colores institucionales azul/blanco con escudo UdeC | ✅ Respetar paleta institucional como base |
| **Branding** | Presencia consistente de marca UdeC en todos los elementos | ✅ Integrar logo/escudo UdeC con identidad departamental |

### 2.4 — [admision.udec.cl/ciencias-fisicas](https://admision.udec.cl/ciencias-fisicas/) (Admisión)

| Aspecto | Observación | Adopción |
|---|---|---|
| **Carrera** | Info de Cs. Físicas: campus, grado, título, especialidades | ✅ Integrar datos curriculares completos |
| **Malla curricular** | Enlace a PDF descargable | ✅ Malla interactiva en HTML + PDF descargable |
| **Puntajes** | Corte 2024: 701.9 · 2023: 691.05 | ✅ Mostrar puntajes históricos con gráfica |
| **Campo ocupacional** | Universidades, centros de investigación, empresas | ✅ Sección dedicada con testimonios |
| **Tabs de contenido** | Malla, Puntajes, Campo, Arancel separados en pestañas | ✅ Componente tabs interactivo |

---

## 3. Estándares de Diseño (IEEE Informatics + WCAG 2.2)

### 3.1 — Principios Fundamentales del Diseño Web Académico

Basado en la investigación de mejores prácticas IEEE y estándares internacionales:

#### A. Accesibilidad — WCAG 2.2 Level AA (Obligatorio)

| Criterio | Implementación |
|---|---|
| **Perceivable** | Alt text en imágenes, captions en video, contraste ≥ 4.5:1 |
| **Operable** | Navegación completa por teclado, skip links, focus visible |
| **Understandable** | Lenguaje claro, mensajes de error descriptivos, labels en formularios |
| **Robust** | HTML semántico, ARIA labels correctos, compatible con screen readers |

#### B. Arquitectura de Información — Centrada en el Usuario

```
Audiencias primarias:
├── Estudiantes actuales  → Horarios, notas, trámites
├── Postulantes           → Carrera, admisión, malla, puntajes
├── Investigadores        → Publicaciones, laboratorios, colaboración
├── Académicos/Staff      → Directorio, contacto, recursos internos
└── Público general       → Noticias, eventos, divulgación científica
```

#### C. Regla de Color 60-30-10

```
60% — Superficie/Fondo:  #0D1117 (dark) | #F8F9FA (light)
30% — Marca/Estructura:  #003366 (UdeC) + #0A6EBD (Física)
10% — Acento/CTA:        #F0C14B (dorado) + #2EA043 (éxito)
```

#### D. Tipografía

| Rol | Fuente | Peso | Tamaño |
|---|---|---|---|
| **Headings** | Inter | 700 (Bold) | H1: 3rem · H2: 2.25rem · H3: 1.75rem |
| **Body** | Inter | 400 (Regular) | 1rem (16px) base |
| **Monospace** | JetBrains Mono | 400 | 0.875rem |
| **Caption** | Inter | 300 (Light) | 0.75rem |

#### E. Espaciado y Grid

| Token | Valor | Uso |
|---|---|---|
| `--space-xs` | 0.25rem | Separación mínima |
| `--space-sm` | 0.5rem | Padding interno |
| `--space-md` | 1rem | Espaciado estándar |
| `--space-lg` | 2rem | Separación de secciones |
| `--space-xl` | 4rem | Margin entre bloques |
| `--space-2xl` | 8rem | Separación heroica |

Grid: CSS Grid con 12 columnas · Max-width: 1280px · Breakpoints: 480/768/1024/1280px

#### F. Micro-animaciones

| Elemento | Animación | Duración |
|---|---|---|
| Hover en links | Color transition | 200ms ease |
| Hover en cards | Scale + shadow | 300ms ease-out |
| Scroll reveal | Fade-in + translateY | 600ms ease |
| Menu toggle | Slide + opacity | 250ms ease |
| Page transition | Fade | 200ms ease |

---

## 4. Arquitectura Técnica — Flask

### 4.1 — Patrón Application Factory

```python
# app/__init__.py
from flask import Flask

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # Registrar blueprints
    from app.routes.main import main_bp
    from app.routes.academics import academics_bp
    from app.routes.research import research_bp
    from app.routes.people import people_bp
    from app.routes.news import news_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(academics_bp, url_prefix='/academics')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(people_bp, url_prefix='/people')
    app.register_blueprint(news_bp, url_prefix='/news')
    
    return app
```

### 4.2 — Mapa de Rutas Planificado

| Ruta | Blueprint | Página |
|---|---|---|
| `/` | main | Inicio |
| `/about` | main | Sobre el departamento |
| `/contact` | main | Contacto |
| `/academics/undergraduate` | academics | Pregrado — Ciencias Físicas |
| `/academics/graduate` | academics | Postgrado (Magíster + Doctorado) |
| `/academics/curriculum` | academics | Malla curricular interactiva |
| `/research` | research | Líneas de investigación |
| `/research/publications` | research | Publicaciones científicas |
| `/research/labs` | research | Laboratorios |
| `/people` | people | Directorio de académicos |
| `/people/<slug>` | people | Perfil individual |
| `/news` | news | Listado de noticias |
| `/news/<slug>` | news | Noticia individual |

### 4.3 — Despliegue en Vercel (Futuro)

```json
// vercel.json
{
  "version": 2,
  "builds": [
    { "src": "run.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "run.py" }
  ]
}
```

---

## 5. Plan de Trabajo — Sprints

### Sprint 0 — Fundamentos (Actual)

- [x] Crear repositorio y estructura de proyecto
- [x] Crear entorno virtual Python (`.venv`)
- [x] Crear README del proyecto
- [x] Crear documento de Kickoff (este documento)
- [ ] Instalar Flask y dependencias base
- [ ] Configurar Application Factory
- [ ] Crear template base (`base.html`) con design system
- [ ] Implementar design system CSS (tokens, variables, componentes)

### Sprint 1 — Home Page + Navegación

- [ ] Hero section con animación de partículas/ondas
- [ ] Menú de navegación responsive con mega-menú
- [ ] Sección de cifras clave del departamento
- [ ] Grid de noticias destacadas (datos mock)
- [ ] Footer con contacto y redes sociales
- [ ] Dark/Light mode toggle
- [ ] Skip links y estructura semántica

### Sprint 2 — Páginas de Contenido

- [ ] Página "Departamento" (historia, misión, organigrama)
- [ ] Directorio de académicos con cards
- [ ] Página de pregrado con malla curricular interactiva
- [ ] Página de postgrado
- [ ] Integración de datos JSON

### Sprint 3 — Investigación + Noticias

- [ ] Página de líneas de investigación
- [ ] Página de publicaciones con filtrado
- [ ] Sistema de noticias con paginación
- [ ] Calendario de seminarios/eventos
- [ ] Página individual de noticia

### Sprint 4 — Pulido + Despliegue

- [ ] Optimización de rendimiento (Lighthouse ≥ 90)
- [ ] Testing accessibility (axe-core, NVDA)
- [ ] SEO meta tags en todas las páginas
- [ ] Configuración de Vercel
- [ ] Deploy a producción
- [ ] Documentación final

---

## 6. Componentes UI Planificados

### Cards (Noticias)

```
┌─────────────────────────────┐
│  ┌───────────────────────┐  │
│  │    Imagen thumbnail   │  │
│  └───────────────────────┘  │
│  📅 27 Mar 2026             │
│  ▎ Categoría                │
│                             │
│  Título de la Noticia       │
│                             │
│  Resumen breve del          │
│  contenido de la noticia... │
│                             │
│  [Leer más →]               │
└─────────────────────────────┘
```

### Hero Section

```
┌─────────────────────────────────────────────┐
│                                             │
│  ┌─ Navbar ──────────────────────────────┐  │
│  │ Logo  │ Nav links │ 🔍 │ 🌙 │ ES/EN │  │
│  └───────────────────────────────────────┘  │
│                                             │
│        DEPARTAMENTO DE FÍSICA               │
│        ═══════════════════════              │
│                                             │
│    Formamos científicas y científicos       │
│    capaces de comprender, investigar y      │
│    transformar el mundo a través de la      │
│    física.                                  │
│                                             │
│    [ Conoce nuestra investigación ]         │
│    [ Postula a Ciencias Físicas   ]         │
│                                             │
│  ╔═ Cifras ════════════════════════════╗    │
│  ║ 45+ Académicos │ 200+ Estudiantes  ║    │
│  ║ 15 Labs        │ 300+ Papers       ║    │
│  ╚════════════════════════════════════╝    │
│                                             │
└─────────────────────────────────────────────┘
```

### Directorio Académico

```
┌──────────┬─────────────────────────┐
│          │  Dr. Nombre Apellido    │
│  📷      │  Profesor Asociado      │
│  Foto    │  Área: Física Teórica   │
│          │  📧 email@udec.cl       │
│          │  [Ver perfil →]         │
└──────────┴─────────────────────────┘
```

---

## 7. Notas Técnicas

### Diferencias con FLAMEweb (Proyecto de Referencia)

| Aspecto | FLAMEweb | CsFisicasWEB |
|---|---|---|
| **Framework** | Vite + TypeScript | Python Flask + Jinja2 |
| **CSS** | TailwindCSS 3.x | Vanilla CSS (Design System propio) |
| **Deploy** | SFTP a servidor UdeC | Vercel (serverless) |
| **Contenido** | JSON estático | JSON + potencial CMS futuro |
| **Testing** | Vitest + Playwright | pytest + Selenium (futuro) |

### Requisitos de Infraestructura Vercel

- Flask app empaquetada como serverless function
- Archivos estáticos servidos por CDN de Vercel
- `vercel.json` con rutas configuradas
- Variables de entorno en dashboard de Vercel

---

## 8. Referencias Bibliográficas

1. **WCAG 2.2** — W3C Web Content Accessibility Guidelines. [w3.org/WAI/WCAG22](https://www.w3.org/WAI/WCAG22/quickref/)
2. **IEEE Standard for Web-Based User Interfaces** — Principios de usabilidad y accesibilidad para sitios académicos.
3. **European Accessibility Act (EAA)** — EN 301 549, estándares de accesibilidad digital.
4. **Google Lighthouse** — Métricas de rendimiento web. [developers.google.com/web/tools/lighthouse](https://developers.google.com/web/tools/lighthouse)
5. **Flask Documentation** — [flask.palletsprojects.com](https://flask.palletsprojects.com/)

---

> **Próximo paso:** Instalar Flask, configurar la Application Factory y construir el design system CSS con los tokens definidos en este documento.

---

*Documento generado el 31 de marzo de 2026 a las 11:28 hrs (CLT)*  
*Autor: Proyecto CsFisicasWEB — Departamento de Física, Universidad de Concepción*
