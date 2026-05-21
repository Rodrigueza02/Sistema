# 📚 Manual de Configuración y Ejecución - Sistema de Gestión Académica (SGA)

## 📋 Tabla de Contenidos
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación Local](#instalación-local)
3. [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
4. [Configuración de Base de Datos](#configuración-de-base-de-datos)
5. [Ejecución del Proyecto](#ejecución-del-proyecto)
6. [Acceso al Sistema](#acceso-al-sistema)
7. [Despliegue en Producción](#despliegue-en-producción)
8. [Solución de Problemas](#solución-de-problemas)

---

### Verificar Instalación
```bash
# Verificar Python
python --version
# Debe mostrar: Python 3.10.x o superior

# Verificar pip
pip --version

# Verificar Git
git --version
```

---

## 💻 Instalación Local

### 1. Clonar el Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/Rodrigueza02/Sistema.git

# Entrar al directorio
cd Sistema
```

### 2. Crear Entorno Virtual

El entorno virtual aísla las dependencias del proyecto.

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verificar activación:**
- Debe aparecer `(venv)` al inicio de la línea de comandos

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales instaladas:**
- Django 4.2.7 - Framework web
- django-environ - Gestión de variables de entorno
- django-crispy-forms - Formularios con estilos
- Pillow - Manejo de imágenes
- reportlab - Generación de PDFs
- openpyxl - Exportación a Excel
- whitenoise - Servir archivos estáticos

---

## ⚙️ Configuración de Variables de Entorno

### 1. Crear Archivo `.env`

Navegar a la carpeta `sistema_academico/` y crear el archivo `.env`:

```bash
cd sistema_academico
```

**Contenido del archivo `.env`:**

```env
# ============================================
# CONFIGURACIÓN DE DJANGO
# ============================================
SECRET_KEY=django-insecure-sga-2026-helen-juliana-proyecto-final-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================
# BASE DE DATOS
# ============================================
DATABASE_URL=sqlite:///db.sqlite3

# ============================================
# CONFIGURACIÓN DE EMAIL (OPCIONAL)
# ============================================
# Para notificaciones de calificaciones
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# ============================================
# NOTAS:
# - Este archivo NO se sube a GitHub
# - Para producción, cambiar SECRET_KEY y DEBUG=False
# ============================================
```

### 2. Configuración de Email 

1. **Usar Gmail:**
   - Ir a tu cuenta de Google
   - Activar "Verificación en 2 pasos"
   - Generar una "Contraseña de aplicación"
   - Usar esa contraseña en `EMAIL_HOST_PASSWORD`

2. **Actualizar `.env`:**
```env
EMAIL_HOST_USER=julirodriguezandrade@gmail.com
EMAIL_HOST_PASSWORD=-contraseña-de-aplicacion
```

---

## 🗄️ Configuración de Base de Datos

### 1. Aplicar Migraciones

Las migraciones crean las tablas en la base de datos.

```bash
# Asegurarse de estar en la carpeta sistema_academico/
cd sistema_academico

# Crear archivos de migración
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

**Salida esperada:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying academic.0001_initial... OK
  ...
```

### 2. Crear Superusuario (Administrador)

```bash
python manage.py createsuperuser
```

**Datos a ingresar:**
- **Username:** admin (o el que prefieras)
- **Email:** admin@sga.com
- **Password:** (mínimo 8 caracteres)
- **Password (again):** (repetir contraseña)

### 3. Cargar Datos de Prueba (Opcional)

Archivo de fixtures con datos de prueba:

```bash
python manage.py loaddata datos_prueba.json
```

---

## 🚀 Ejecución del Proyecto

### 1. Iniciar Servidor de Desarrollo

```bash
# Asegurarse de estar en sistema_academico/
python manage.py runserver
```

**Salida esperada:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 18, 2026 - 15:30:00
Django version 4.2.7, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 2. Acceder al Sistema

Abrir el navegador y visitar:
- **Aplicación principal:** http://127.0.0.1:8000/
- **Panel de administración:** http://127.0.0.1:8000/admin/
- **Login:** http://127.0.0.1:8000/accounts/login/

### 3. Detener el Servidor

Presionar `CTRL + C` en la terminal

---

## 🔐 Acceso al Sistema

### Credenciales de Acceso al Dashboard Web

Credenciales reales del sistema desplegado.

#### Producción (Render)
- **URL:** https://sistema-academico-qiuh.onrender.com/
- **Usuario Administrador:**
  - Username: `_admin____`
  - Password: `__Admin2026*___`
- **Usuario Docente:**
  - Username: `_FernandaDocente______________`
  - Password: `_Malua.230225______`
- **Usuario Estudiante:**
  - Username: `___helenestudiante_______`
  - Password: `__Malua.230225_____`

#### Desarrollo Local
- **URL:** http://127.0.0.1:8000/
- **Superusuario:**
  - Username: `admin`
  - Password: `(Admin2026*)`

### Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **Administrador** | Acceso total: gestión de usuarios, materias, cursos, notas, asistencia |
| **Docente** | Gestión de notas y asistencia de sus materias asignadas |
| **Estudiante** | Visualización de sus propias notas y asistencia |

---

## 🌐 Despliegue en Producción

### Plataforma: Render

#### 1. Preparar el Proyecto

**Crear archivo `build.sh` en la raíz:**
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd sistema_academico
python manage.py collectstatic --no-input
python manage.py migrate
```

**Dar permisos de ejecución:**
```bash
chmod +x build.sh
```

#### 2. Configurar Variables de Entorno en Render

En el panel de Render, agregar:
```
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com
DATABASE_URL=postgresql://... (Render lo proporciona)
```

#### 3. Configurar `settings.py` para Producción

```python
# En config/settings.py
import dj_database_url

if not DEBUG:
    DATABASES['default'] = dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=600
    )
```

#### 4. Crear Superusuario en Producción

Desde la consola de Render:
```bash
python sistema_academico/manage.py createsuperuser
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'django'"

**Causa:** El entorno virtual no está activado o Django no está instalado.

**Solución:**
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### Error: "django.db.utils.OperationalError: no such table"

**Causa:** Las migraciones no se han aplicado.

**Solución:**
```bash
cd sistema_academico
python manage.py migrate
```

### Error: "CSRF verification failed"

**Causa:** Problema con cookies o configuración de CSRF.

**Solución:**
1. Limpiar cookies del navegador
2. Verificar que `ALLOWED_HOSTS` incluya el dominio correcto
3. Usar modo incógnito para probar

### Error: "Port 8000 is already in use"

**Causa:** Otro proceso está usando el puerto 8000.

**Solución:**
```bash
# Usar otro puerto
python manage.py runserver 8080

# O detener el proceso que usa el puerto 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000
```

### Error al enviar emails

**Causa:** Configuración incorrecta de email o credenciales inválidas.

**Solución:**
1. Verificar que `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` estén correctos
2. Si usas Gmail, generar una "Contraseña de aplicación"
3. Verificar que el puerto sea 587 y `EMAIL_USE_TLS=True`

### Error: "Internal Server Error" en producción

**Causa:** `DEBUG=False` oculta los errores detallados.

**Solución:**
1. Revisar logs en Render
2. Verificar que `ALLOWED_HOSTS` incluya el dominio
3. Verificar que `collectstatic` se ejecutó correctamente
4. Revisar que todas las migraciones se aplicaron

---

## 📞 Contacto y Soporte

### Equipo de Desarrollo
- **Helen** - Sistema de Autenticación y Roles
- **Juliana** - Módulo Académico

### Repositorio
- **GitHub:** https://github.com/Rodrigueza02/Sistema

### Documentación Adicional
- **Django:** https://docs.djangoproject.com/
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Render:** https://render.com/docs

---


**Sistema de Gestión Académica - Proyecto Final Django 2026**
