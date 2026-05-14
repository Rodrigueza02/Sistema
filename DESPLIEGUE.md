# Guía de Despliegue — Render

Pasos para publicar el Sistema de Gestión Académica en Render con PostgreSQL gratuito.

---

## 1. Preparar el repositorio

Asegúrate de que estos archivos estén en la raíz del repo (ya están creados):

```
Procfile
render.yaml
requirements.txt
```

Sube todos los cambios a GitHub:

```bash
git add .
git commit -m "feat: proyecto completo listo para despliegue"
git push origin feature/academic-core
```

Luego haz merge a `main` (o pídele a Helen que lo haga si ella maneja `main`).

---

## 2. Crear cuenta en Render

1. Ve a [https://render.com](https://render.com) y crea una cuenta gratuita.
2. Conecta tu cuenta de GitHub cuando te lo pida.

---

## 3. Crear la base de datos PostgreSQL

1. En el dashboard de Render → **New** → **PostgreSQL**
2. Nombre: `sga-db`
3. Plan: **Free**
4. Clic en **Create Database**
5. Copia la **Internal Database URL** (la necesitas en el paso 5)

---

## 4. Crear el servicio web

1. En el dashboard → **New** → **Web Service**
2. Conecta el repositorio de GitHub
3. Configura:

| Campo | Valor |
|---|---|
| Name | `sistema-academico` |
| Root Directory | *(dejar vacío)* |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt && cd sistema_academico && python manage.py collectstatic --noinput` |
| Start Command | `cd sistema_academico && python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| Plan | **Free** |

---

## 5. Configurar variables de entorno

En el servicio web → **Environment** → agrega estas variables:

| Key | Value |
|---|---|
| `SECRET_KEY` | Una clave larga y aleatoria (genera una en [djecrety.ir](https://djecrety.ir)) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `tu-app.onrender.com` |
| `DATABASE_URL` | La URL de PostgreSQL copiada en el paso 3 |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_HOST_USER` | Tu correo Gmail |
| `EMAIL_HOST_PASSWORD` | Tu contraseña de aplicación de Gmail* |

> **Contraseña de aplicación Gmail:** Ve a tu cuenta Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicación → Genera una para "Correo / Windows".

---

## 6. Desplegar

1. Clic en **Create Web Service**
2. Render ejecutará el build automáticamente (tarda ~3 minutos)
3. Cuando diga **Live**, tu app estará en: `https://sistema-academico.onrender.com`

---

## 7. Crear el superusuario en producción

Una vez desplegado, ve a **Shell** en el panel de Render y ejecuta:

```bash
cd sistema_academico && python manage.py createsuperuser
```

---

## 8. Verificar que funciona

Abre la URL pública y prueba:
- [ ] Login con el superusuario
- [ ] Crear una materia
- [ ] Registrar una nota
- [ ] Descargar un boletín PDF
- [ ] Descargar el Excel
- [ ] Ver el dashboard con gráficos

---

## Notas importantes

- El plan gratuito de Render **duerme** el servicio tras 15 min de inactividad. La primera carga puede tardar ~30 segundos.
- La base de datos gratuita de Render tiene límite de 1 GB y expira a los 90 días.
- Para el informe final, toma capturas de pantalla de cada sección funcionando en la URL pública.
