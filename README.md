# Sistema de Gestión Académica (SGA)

Plataforma web para gestionar cursos, estudiantes, docentes y calificaciones desarrollada con Django.

## Equipo de Desarrollo

- Helen- Sistema de Autenticación y Roles (`feature/auth-roles`)
- Juliana- Módulo Académico (`feature/academic-core`)

## Características Principales

### Sistema de Autenticación (Helen)
- [x] Login con roles (Admin, Docente, Estudiante)
- [x] Registro de usuarios
- [x] CRUD de usuarios con control activo/inactivo
- [x] Mixins de permisos por rol
- [x] Notificaciones por correo electrónico
- [x] Base template con sidebar colapsable (Tailwind CSS)

### Módulo Académico (Juliana - En desarrollo)
- [ ] Modelos: Materia, Curso, Nota, Asistencia
- [ ] CRUD completo de cursos, materias y notas
- [ ] Registro de asistencia
- [ ] Dashboard con Chart.js (promedios + asistencia)
- [ ] Exportación PDF/Excel (boletines, actas)
- [ ] Buscador por estudiante o curso

## Requisitos del Sistema

- Python 3.10+
- Django 4.2.7
- SQLite (incluido con Python)

## Instalación

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
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
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

## Estructura del Proyecto

```
sistema_academico/
├── accounts/           # Autenticación y usuarios (Helen)
│   ├── models.py      # CustomUser con roles
│   ├── views.py       # Login, Register, CRUD usuarios
│   ├── mixins.py      # Permisos por rol
│   ├── tasks.py       # Notificaciones email
│   └── urls.py        # URLs de autenticación
├── academic/          # Módulo académico (Juliana)
│   ├── models.py      # Materia, Curso, Nota, Asistencia
│   ├── views.py       # CRUD y lógica de negocio
│   └── urls.py        # URLs del módulo
├── dashboard/         # Panel principal (Juliana)
├── reports/           # Reportes PDF/Excel (Juliana)
├── templates/         # Templates HTML
│   ├── base.html     # Template base con sidebar
│   └── accounts/     # Templates de autenticación
└── config/           # Configuración Django
    ├── settings.py
    └── urls.py
```

## Roles de Usuario

| Rol | Permisos |
|-----|----------|
| **Admin** | Acceso total al sistema, gestión de usuarios |
| **Docente** | Gestión de cursos, notas y asistencia |
| **Estudiante** | Visualización de notas y asistencia |

## Tecnologías Utilizadas

- **Backend:** Django 4.2.7
- **Frontend:** Tailwind CSS, Chart.js
- **Base de datos:** SQLite
- **Reportes:** ReportLab (PDF), OpenPyXL (Excel)
- **Email:** SMTP

## Flujo de Trabajo Git

### Ramas principales
- `main` - Producción
- `develop` - Desarrollo
- `feature/auth-roles` - Helen (Autenticación)
- `feature/academic-core` - Juliana (Módulo académico)

### Comandos útiles

```bash
# Ver ramas
git branch -a

# Cambiar de rama
git checkout feature/auth-roles

# Actualizar desde develop
git pull origin develop

# Subir cambios
git add .
git commit -m "feat: descripción del cambio"
git push origin feature/auth-roles
```

## Contacto

- **Helen** - Sistema de Autenticación
- **Juliana** - Módulo Académico

---

**Proyecto Final - Django 2026** 
