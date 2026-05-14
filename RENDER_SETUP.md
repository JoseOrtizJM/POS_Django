# 📖 Guía de Despliegue en Render con Cloudflare

## Paso 1: Preparar tu Repositorio Git

```bash
# Inicializar git si aún no lo has hecho
git init
git add .
git commit -m "Preparación para producción"
```

## Paso 2: Subir a un Repositorio Remoto

```bash
# Crear un repositorio en GitHub, GitLab o Bitbucket
# Luego:
git remote add origin <URL_DEL_REPOSITORIO>
git branch -M main
git push -u origin main
```

## Paso 3: Crear una Base de Datos PostgreSQL en Render

1. Ve a [render.com](https://render.com)
2. Haz clic en **+ New** → **PostgreSQL**
3. Configura:
   - **Name**: `pos-database` (o similar)
   - **Region**: Elige la más cercana a ti
   - **PostgreSQL Version**: 15
4. Copia la **Internal Database URL** (la necesitarás después)

## Paso 4: Crear una Aplicación Web en Render

1. Haz clic en **+ New** → **Web Service**
2. Selecciona tu repositorio Git
3. Configura:
   - **Name**: `pos-django` (o similar)
   - **Region**: Igual a la de tu base de datos
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn POS_Django.wsgi:application`

## Paso 5: Agregar Variables de Entorno en Render

En la página de tu aplicación, ve a **Environment** y agrega estas variables:

```
SECRET_KEY=<GENERA_UNA_NUEVA_CON: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'>

DEBUG=False

ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,nombre-en-render.onrender.com

DB_NAME=<nombre_de_la_bd_desde_postgres>
DB_USER=<usuario_desde_postgres>
DB_PASSWORD=<contraseña_desde_postgres>
DB_HOST=<host_internal_desde_postgres>
DB_PORT=5432

GOOGLE_CLIENT_ID=<tu_client_id>
GOOGLE_CLIENT_SECRET=<tu_client_secret>
GOOGLE_REDIRECT_URI=https://tu-dominio.com/usuarios/google/callback/

EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=<contraseña_de_aplicación_de_google>
DEFAULT_FROM_EMAIL=Mayorista <tu-email@gmail.com>
EMAIL_NOTIFICACIONES_ENABLED=True
```

## Paso 6: Configurar Cloudflare

### A. Apuntar tu dominio a Render

1. En Cloudflare, ve a **DNS** → **Records**
2. Crea/edita un registro **CNAME**:
   - **Name**: `www` (o `@` para el dominio raíz)
   - **Content**: El dominio que Render te asignó (ej: `pos-django.onrender.com`)
   - **TTL**: Auto
   - **Proxy status**: Proxied (naranja)

3. Si usas el dominio sin `www`, crea también un registro:
   - **Name**: `@`
   - **Content**: Tu dominio de Render

### B. Configurar SSL/TLS

1. En Cloudflare, ve a **SSL/TLS** → **Overview**
2. Asegúrate que esté en modo **Full** o **Full (strict)**
3. Ve a **Edge Certificates** y habilita:
   - ✅ Always Use HTTPS
   - ✅ HTTP Strict Transport Security (HSTS)

### C. Reglas de Reescritura (Opcional pero recomendado)

Ve a **Rules** → **Page Rules** y agrega:
- **URL Pattern**: `http://tu-dominio.com/*`
- **Settings**: 
  - **Always Use HTTPS**: On

## Paso 7: Actualizar ALLOWED_HOSTS y configuraciones Django

Asegúrate de que `ALLOWED_HOSTS` en Render incluya:
- Tu dominio principal
- www.tu-dominio.com
- El dominio de Render (para testing)

## Paso 8: Ejecutar Migraciones

Una vez que tu aplicación se despliegue, las migraciones correrán automáticamente con el `Build Command`.

Si necesitas ejecutar comandos adicionales:
1. En Render, ve a tu aplicación
2. Haz clic en **Shell** (arriba a la derecha)
3. Ejecuta: `python manage.py <comando>`

## Paso 9: Monitorear Logs

En Render, ve a **Logs** para ver:
- Errores de despliegue
- Errores de aplicación
- Requests HTTP

---

## ⚠️ Checklist Final

- [ ] Repositorio Git creado y sincronizado
- [ ] Base de datos PostgreSQL creada en Render
- [ ] Aplicación web creada en Render
- [ ] Variables de entorno configuradas
- [ ] Dominio apuntando correctamente en Cloudflare
- [ ] SSL/TLS habilitado en Cloudflare
- [ ] ALLOWED_HOSTS actualizado
- [ ] Primera compilación completada sin errores
- [ ] Puedes acceder a tu dominio sin errores

---

## 🔍 Solución de Problemas

### Problema: "DisallowedHost at /"
**Solución**: Verifica que tu dominio esté en `ALLOWED_HOSTS` en las variables de entorno de Render.

### Problema: Error de conexión a base de datos
**Solución**: 
1. Verifica que DB_HOST, DB_USER, DB_PASSWORD sean correctos
2. Asegúrate de que el host sea el **Internal Database URL**
3. En Render, conecta la base de datos a tu aplicación web desde el panel

### Problema: Static files no carga
**Solución**: 
- Asegúrate que `collectstatic` corra en el Build Command
- Verifica que `STATIC_URL` y `STATIC_ROOT` sean correctos

### Problema: El dominio de Cloudflare muestra error
**Solución**:
1. Verifica el registro CNAME en Cloudflare
2. Espera 24-48 horas para propagación de DNS
3. Prueba con el dominio de Render directamente primero
