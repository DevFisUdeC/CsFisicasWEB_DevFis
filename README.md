# CsFisicasWEB — Departamento de Física · UdeC

> Rediseño integral del sitio web del **Departamento de Física** de la Facultad de Ciencias Físicas y Matemáticas, Universidad de Concepción.

**Objetivo:** Reemplazar la actual página [fisica.udec.cl](https://fisica.udec.cl/) —basada en WordPress/Kubio con desempeño deficiente— por una aplicación web moderna, elegante y orientada a la academia, desarrollada con **Python Flask** para servicio local y despliegue futuro en **Vercel**.

---

## 🎯 Visión del Proyecto

Crear una experiencia digital de nivel premium que represente la excelencia académica e investigativa del Departamento de Física, siguiendo estándares internacionales de diseño web (IEEE Informatics, WCAG 2.2) y tomando como referencia las mejores prácticas observadas en sitios homólogos de la Universidad de Concepción.

### Sitios de Referencia

| Sitio | URL | Relevancia |
|---|---|---|
| Facultad CFM | [cfm.cl](https://www.cfm.cl/) | Estructura de navegación, noticias, departamentos |
| Facultad de Ingeniería | [fi.udec.cl](https://fi.udec.cl/) | Diseño moderno, cifras, agenda, accesibilidad |
| Universidad de Concepción | [udec.cl](https://www.udec.cl/) | Identidad institucional, paleta de colores |
| Admisión Cs. Físicas | [admision.udec.cl/ciencias-fisicas](https://admision.udec.cl/ciencias-fisicas/) | Contenido curricular, campo ocupacional |

---

## 🛠️ Stack Tecnológico

### Core

| Tecnología | Versión | Propósito |
|---|---|---|
| **Python** | 3.11+ | Lenguaje del servidor |
| **Flask** | 3.x | Framework web (micro) |
| **Jinja2** | 3.x | Motor de templates |
| **HTML5** | — | Estructura semántica |
| **CSS3 (Vanilla)** | — | Estilos y diseño visual |
| **JavaScript (ES6+)** | — | Interactividad del cliente |

### Tipografía & Diseño (IEEE Informatics Guidelines)

| Elemento | Especificación |
|---|---|
| **Fuente principal** | Inter / Outfit (Google Fonts) |
| **Fuente secundaria** | JetBrains Mono (código/datos) |
| **Tamaño base** | 16 px mínimo (WCAG 2.2) |
| **Contraste mínimo** | 4.5:1 texto normal · 3:1 texto grande |
| **Regla de color** | 60-30-10 (Neutro–Marca–Acento) |

### Paleta de Colores (Propuesta)

```
Primario (UdeC):      #003366  — Azul institucional oscuro
Secundario (Física):  #0A6EBD  — Azul ciencia vibrante
Acento:               #F0C14B  — Dorado/ámbar académico
Superficie oscura:    #0D1117  — Fondo dark mode
Superficie clara:     #F8F9FA  — Fondo light mode
Texto principal:      #E6EDF3  — Texto sobre fondo oscuro
Texto secundario:     #8B949E  — Texto auxiliar
Éxito:                #2EA043  — Estados positivos
Advertencia:          #D29922  — Estados de alerta
Error:                #F85149  — Estados de error
```

### DevOps

| Herramienta | Propósito |
|---|---|
| **Git + GitHub** | Control de versiones |
| **Vercel** | Despliegue en producción (futuro) |
| **venv** | Entorno virtual Python |

---

## 📁 Estructura del Proyecto (Planificada)

```
CsFisicasWEB/
├── .venv/                  # Entorno virtual Python
├── app/
│   ├── __init__.py         # Factory de la aplicación Flask
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py         # Rutas principales (Home, About)
│   │   ├── academics.py    # Pregrado, postgrado, malla
│   │   ├── research.py     # Investigación, publicaciones
│   │   ├── people.py       # Académicos, staff
│   │   └── news.py         # Noticias, eventos
│   ├── templates/
│   │   ├── base.html       # Layout maestro con nav/footer
│   │   ├── components/     # Componentes Jinja2 reutilizables
│   │   └── pages/          # Templates de cada página
│   ├── static/
│   │   ├── css/
│   │   │   ├── design-system.css   # Tokens y variables CSS
│   │   │   ├── components.css      # Estilos de componentes
│   │   │   ├── layout.css          # Grid y estructura
│   │   │   └── animations.css      # Micro-animaciones
│   │   ├── js/
│   │   │   ├── main.js             # Lógica principal
│   │   │   ├── navigation.js       # Menú responsive
│   │   │   └── animations.js       # Scroll y hover effects
│   │   ├── img/                    # Imágenes optimizadas
│   │   └── fonts/                  # Fuentes locales (fallback)
│   └── data/
│       ├── team.json               # Académicos y staff
│       ├── research.json           # Líneas de investigación
│       ├── programs.json           # Programas académicos
│       └── config.json             # Configuración del sitio
├── Docs/                           # Documentación del proyecto
├── tests/                          # Tests unitarios y E2E
├── requirements.txt                # Dependencias Python
├── config.py                       # Configuración Flask
├── run.py                          # Entry point de desarrollo
├── vercel.json                     # Configuración de Vercel
├── .gitignore
├── .env                            # Variables de entorno (NO commit)
└── README.md                       # Este archivo
```

---

## 🚀 Quick Start

### Prerrequisitos

- **Python** 3.11+
- **pip** (incluido con Python)
- **Git**

### Instalación

```powershell
# 1. Clonar el repositorio
git clone <repo-url>
cd CsFisicasWEB

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales
```

### Desarrollo Local

```powershell
# Iniciar servidor de desarrollo con hot reload
python run.py

# Abrir http://localhost:5000
```

### Despliegue en Vercel (Futuro)

```powershell
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

---

## 📐 Principios de Diseño (IEEE Informatics)

### 1. Accesibilidad (WCAG 2.2 Level AA)

- HTML semántico (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`)
- Skip links para navegación con teclado
- Atributos ARIA en elementos interactivos
- Alt text descriptivo en todas las imágenes
- Contraste de color verificado (≥ 4.5:1)
- Fuente legible con tamaño mínimo 16 px

### 2. Navegación Centrada en el Usuario

- Arquitectura basada en audiencias: estudiantes, académicos, investigadores, postulantes
- Menú principal intuitivo con mega-menú para subpáginas
- Barra de búsqueda prominente
- Breadcrumbs en páginas internas
- Footer con enlaces rápidos y contacto

### 3. Excelencia Visual

- **Dark mode** como modo principal (elegancia académica)
- Glassmorphism en tarjetas y paneles
- Gradientes suaves con la paleta institucional
- Micro-animaciones en scroll y hover
- Tipografía moderna con jerarquía clara (H1–H6)
- Regla 60-30-10 para distribución de color

### 4. Rendimiento

- CSS modular (sin frameworks pesados)
- Imágenes optimizadas (WebP, lazy loading)
- Fuentes con `font-display: swap`
- Diseño mobile-first responsive
- Score objetivo: Lighthouse ≥ 90 en todas las métricas

---

## 📝 Secciones Planificadas del Sitio

| Sección | Descripción |
|---|---|
| **Inicio** | Hero con misión del departamento, noticias destacadas, cifras clave |
| **Departamento** | Historia, misión/visión, organigrama, reglamentos |
| **Académicos** | Directorio de profesores con foto, área, publicaciones |
| **Pregrado** | Carrera de Ciencias Físicas, malla curricular, admisión |
| **Postgrado** | Magíster, Doctorado, reglamentos, postulación |
| **Investigación** | Líneas de investigación, laboratorios, publicaciones |
| **Noticias** | Feed de noticias y eventos del departamento |
| **Contacto** | Formulario, ubicación, horarios, redes sociales |

---

## 📚 Documentación

| Documento | Descripción |
|---|---|
| [Kickoff — 31 Marzo 2026](./Docs/20260331_1128_KICKOFF_Cs_Fisicas_Web.md) | Documento inaugural del proyecto |
| Guía de Estilos | *(próximamente)* |
| Guía de Contenido | *(próximamente)* |
| Reporte de Sprint | *(próximamente)* |

---

## 🔒 Seguridad

- Nunca hacer commit de archivos `.env`
- Mantener credenciales seguras
- Seguir mejores prácticas de seguridad web
- Reportar vulnerabilidades al equipo responsable

---

## 📄 Licencia

© 2026 Departamento de Física — Facultad de Ciencias Físicas y Matemáticas — Universidad de Concepción. Todos los derechos reservados.

---

**Versión:** 0.1.0  
**Última actualización:** 31 de marzo de 2026  
**Autor:** Proyecto CsFisicasWEB  
