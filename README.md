# Sistema de Gestión Académica (SGA)

Plataforma web para gestionar cursos, estudiantes, docentes y calificaciones, desarrollada con Django y Tailwind CSS.

## Equipo de Desarrollo

| Desarrolladora | Rama | Módulo |
|---|---|---|
| Helen | `feature/auth-roles` | Autenticación, roles y usuarios |
| Juliana | `feature/academic-core` | Módulo académico, dashboard y reportes |

---

## Características implementadas

### Sistema de Autenticación (Helen)
- [x] Login con roles: Admin, Docente, Estudiante
- [x] Registro de usuarios
- [x] CRUD de usuarios con control activo/inactivo
- [x] Mixins de permisos por rol (`SoloAdminMixin`, `DocenteOAdminMixin`)
- [x] Notificaciones por correo al registrar notas
- [x] Base template con sidebar colapsable (Tailwind CSS)

### Módulo Académico (Juliana)
- [x] Modelos: Materia, Curso, Nota, Asistencia
- [x] CRUD completo de materias, cursos, notas y asistencia
- [x] Registro de asistencia con estado presente/ausente
- [x] Dashboard con Chart.js (promedio por materia + asistencia mensual)
- [x] Boletín PDF individual con filtro por fechas
- [x] Acta PDF de curso completo (todos los estudiantes)
- [x] Exportación Excel con filtros (fecha, materia, curso) — 2 hojas: Notas + Asistencia
- [x] Buscador por estudiante o curso con estado activo/inactivo
- [x] Panel de reportes con interfaz de filtros

---

## Requisitos del sistema

- Python 3.10+
- Django 4.2+
- SQLite (desarrollo) / PostgreSQL (producción)

## Instalación local

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd sistema-academico
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en `sistema_academico/`:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-correo@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### 5. Aplicar migraciones

```bash
cd sistema_academico
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000`

---

## Despliegue en Render

### 1. Archivos necesarios (ya incluidos)

- `Procfile` — comando de inicio para Render/Railway
- `render.yaml` — configuración de servicio web
- `requirements.txt` — dependencias

### 2. Variables de entorno en Render

Configurar en el panel de Render → Environment:

```
SECRET_KEY=<generar una clave segura>
DEBUG=False
ALLOWED_HOSTS=<tu-app>.onrender.com
DATABASE_URL=<url de PostgreSQL de Render>
EMAIL_HOST_USER=<correo>
EMAIL_HOST_PASSWORD=<app password>
```

### 3. Comandos de build en Render

```bash
pip install -r requirements.txt
cd sistema_academico && python manage.py collectstatic --noinput && python manage.py migrate
```

---

## Estructura del proyecto

```
sistema_academico/
├── accounts/           # Autenticación y usuarios (Helen)
│   ├── models.py      # CustomUser con roles
│   ├── views.py       # Login, Register, CRUD usuarios
│   ├── mixins.py      # Permisos por rol
│   ├── tasks.py       # Notificaciones email
│   └── urls.py
├── academic/          # Módulo académico (Juliana)
│   ├── models.py      # Materia, Curso, Nota, Asistencia
│   ├── views.py       # CRUD + APIs JSON para Chart.js
│   ├── forms.py       # Formularios validados
│   └── urls.py
├── dashboard/         # Panel principal (Juliana)
│   ├── views.py       # DashboardView con estadísticas
│   └── urls.py
├── reports/           # Reportes PDF/Excel (Juliana)
│   ├── views.py       # Boletín PDF, Acta PDF, Excel
│   └── urls.py
├── templates/
│   ├── base.html      # Template base con sidebar
│   ├── accounts/      # Login, register, usuarios
│   ├── academic/      # CRUD materias, cursos, notas, asistencia, buscador
│   ├── dashboard/     # index.html con Chart.js
│   └── reports/       # Página de reportes con filtros
└── config/
    ├── settings.py
    └── urls.py
```

## Modelos principales

| Modelo | Campos clave | Relaciones |
|---|---|---|
| `CustomUser` | rol, activo, telefono | — |
| `Materia` | nombre, codigo, creditos, activa | FK → CustomUser (docente) |
| `Curso` | nombre, año, periodo | M2M → Materia, M2M → CustomUser |
| `Nota` | valor, tipo, fecha | FK → Estudiante, Materia, Curso |
| `Asistencia` | fecha, presente | FK → Estudiante, Materia, Curso |

## Rutas principales

| URL | Vista | Descripción |
|---|---|---|
| `/dashboard/` | DashboardView | Panel con gráficos |
| `/academic/materias/` | MateriaListView | Lista de materias |
| `/academic/cursos/` | CursoListView | Lista de cursos |
| `/academic/notas/` | NotaListView | Lista de notas |
| `/academic/asistencia/` | AsistenciaListView | Registro de asistencia |
| `/academic/buscar/` | BuscadorView | Buscador global |
| `/reports/` | ReportesView | Panel de reportes |
| `/reports/boletin/<id>/pdf/` | BoletinPDFView | PDF individual |
| `/reports/acta/<id>/pdf/` | ActaCursoPDFView | Acta de curso |
| `/reports/notas/excel/` | ReporteExcelView | Excel con filtros |
| `/api/promedios/` | promedios_por_materia | JSON para Chart.js |
| `/api/asistencia/` | asistencia_mensual | JSON para Chart.js |

## Roles de usuario

| Rol | Permisos |
|---|---|
| **Admin** | Acceso total: CRUD completo, gestión de usuarios |
| **Docente** | Registrar notas y asistencia, ver reportes |
| **Estudiante** | Ver sus propias notas y asistencia |

## Tecnologías utilizadas

- **Backend:** Django 4.2
- **Frontend:** Tailwind CSS, Chart.js, Font Awesome
- **Base de datos:** SQLite (dev) / PostgreSQL (prod)
- **Reportes:** ReportLab (PDF), OpenPyXL (Excel)
- **Email:** SMTP (Gmail)
- **Despliegue:** Render / Railway

---

*Proyecto Final — Django 2026 — Helen & Juliana*
