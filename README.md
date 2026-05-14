# POS Django — Sistema de Punto de Venta Mayoreo

Sistema completo de Punto de Venta para gestión de mayoreo de abarrotes, con catálogo, carrito, checkout, panel de administración con reportes y API REST.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-6.0.4-darkgreen?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?style=flat-square)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square)

---

## Características

### Autenticación
- Login y registro con email/contraseña
- **Login con Google** (OAuth 2.0)
- Roles separados: Administrador y Usuario
- Sesiones independientes por rol

### Catálogo de Productos
- 12 categorías con emoji identificador
- 105+ productos con imagen, precio, stock y presentación
- Buscador en tiempo real (AJAX) desde el dashboard
- Buscador dentro de cada categoría
- Placeholder visual con emoji de categoría cuando no hay imagen
- Indicadores de stock (agotado / poco stock)

### Carrito y Checkout
- Widget de cantidad con actualización AJAX
- Carrito persistente por usuario
- Checkout con selección de tarjeta de crédito guardada
- Notificación por correo al confirmar pedido (Gmail SMTP)

### Panel de Administración
- Dashboard con 6 KPIs en tiempo real (ventas del día, semana, mes, productos, clientes, stock bajo)
- Gráfica de ventas con toggle 7 / 30 días (Chart.js)
- Gráfica de métodos de pago (efectivo vs tarjeta)
- Top 5 productos más vendidos del mes
- Tabla de últimas 10 ventas
- Alertas de productos con stock bajo (con imagen)
- Accesos directos a todas las secciones

### CRUD Completo
- **Productos**: crear, editar (con imagen), eliminar, activar/desactivar
- **Categorías**: crear, editar, eliminar
- **Usuarios**: listar, activar/desactivar, búsqueda y filtros

### Reportes de Ventas
- Vista de ventas del día con detalle por venta
- Reporte por período: hoy, semana, mes o rango de fechas personalizado
- Gráfica de ingresos diarios por período
- Top 10 productos por ingresos en el período
- Filtro de ventas por cliente en tiempo real

### Perfil de Usuario
- Edición de datos personales
- Gestión de tarjetas de crédito
- Historial de pedidos (vía API)

### Perfil de Administrador
- Edición de nombre de usuario y correo
- Cambio de contraseña con validación en tiempo real

### API REST
Disponible en `/api/` con autenticación por token JWT:
- Catálogo público (categorías y productos)
- Auth: registro, login, logout (usuarios y admin)
- Carrito y checkout
- Historial de ventas del cliente
- Panel admin: resumen, ventas, usuarios, productos

---

## Requisitos Previos

- Python 3.10+
- PostgreSQL 14+ corriendo en el puerto `5433`
- pip

---

## Instalación

1. **Clonar el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd Django-Final
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv

   # Windows PowerShell
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**

   Crea una base de datos PostgreSQL y un usuario con acceso. Luego edita `POS_Django/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'pos_db',
           'USER': 'pos_user',
           'PASSWORD': 'tu_password',
           'HOST': 'localhost',
           'PORT': '5433',
       }
   }
   ```

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Cargar datos iniciales**
   ```bash
   python manage.py cargar_datos
   ```

7. **Iniciar el servidor**
   ```bash
   python manage.py runserver
   ```

---

## Google OAuth (opcional)

Para habilitar el inicio de sesión con Google:

1. Crea credenciales OAuth 2.0 en [Google Cloud Console](https://console.cloud.google.com)
2. Agrega el URI de redirección: `http://127.0.0.1:8000/usuarios/google/callback/`
3. Configura las variables de entorno antes de iniciar el servidor:

   ```powershell
   # PowerShell
   $env:GOOGLE_CLIENT_ID="TU_CLIENT_ID"
   $env:GOOGLE_CLIENT_SECRET="TU_CLIENT_SECRET"
   python manage.py runserver
   ```

   ```bash
   # Linux / macOS
   export GOOGLE_CLIENT_ID="TU_CLIENT_ID"
   export GOOGLE_CLIENT_SECRET="TU_CLIENT_SECRET"
   python manage.py runserver
   ```

Para producción con dominio propio, agrega también:
```bash
export GOOGLE_REDIRECT_URI="https://tudominio.com/usuarios/google/callback/"
```

---

## Correo Electrónico (opcional)

Configura en `settings.py` con una contraseña de aplicación de Gmail:

```python
EMAIL_HOST_USER     = 'tu@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # Contraseña de aplicación
```

---

## URLs Principales

### Públicas
| URL | Descripción |
|-----|-------------|
| `/` | Catálogo / Dashboard |
| `/categoria/<id>/` | Productos de una categoría |
| `/buscar/` | Búsqueda AJAX de productos |
| `/usuarios/login/` | Inicio de sesión |
| `/usuarios/registro/` | Registro de usuario |
| `/usuarios/google/login/` | Login con Google |

### Usuario autenticado
| URL | Descripción |
|-----|-------------|
| `/usuarios/perfil/` | Perfil del usuario |
| `/usuarios/carrito/` | Carrito de compras |
| `/usuarios/checkout/` | Proceso de compra |
| `/usuarios/tarjetas/` | Mis tarjetas |
| `/usuarios/completar-perfil/` | Completar perfil (Google) |

### Administrador
| URL | Descripción |
|-----|-------------|
| `/administradores/login/` | Login de admin |
| `/administradores/panel/` | Dashboard con KPIs y gráficas |
| `/administradores/productos/` | Gestión de productos |
| `/administradores/categorias/` | Gestión de categorías |
| `/administradores/usuarios/` | Gestión de clientes |
| `/administradores/ventas/` | Ventas del día |
| `/administradores/ventas/reporte/` | Reporte por período |
| `/administradores/perfil/` | Perfil del administrador |

### API REST
| URL | Descripción |
|-----|-------------|
| `/api/categorias/` | Lista de categorías |
| `/api/productos/` | Lista de productos |
| `/api/auth/registro/` | Registro vía API |
| `/api/auth/login/` | Login vía API (devuelve token) |
| `/api/carrito/` | Carrito del usuario |
| `/api/checkout/` | Confirmar pedido |
| `/api/ventas/` | Historial de ventas |
| `/api/admin/resumen/` | Resumen para admin |

---

## Estructura del Proyecto

```
Django-Final/
├── POS_Django/               # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── context_processors.py
├── catalogo/                 # App principal: dashboard y catálogo
│   ├── models.py             # Categoria, Producto
│   ├── views.py              # dashboard, productos_por_categoria, buscar
│   ├── management/commands/cargar_datos.py
│   ├── static/catalogo/
│   │   ├── vendor/           # Bootstrap y FontAwesome locales
│   │   ├── css/
│   │   │   ├── base/         # variables, globals, navbar
│   │   │   ├── components/   # cards, buttons, forms, tables, alerts
│   │   │   └── pages/        # dashboard, catalogo
│   │   └── js/               # utils, carrito, main
│   └── templates/catalogo/
│       ├── base.html
│       ├── dashboard.html
│       └── productos_categoria.html
├── usuarios/                 # App de clientes
│   ├── models.py             # Usuario, TarjetaCredito, Carrito, CarritoItem
│   ├── views.py              # auth, carrito, checkout, perfil, Google OAuth
│   ├── forms.py
│   └── templates/usuarios/
│       ├── login.html
│       ├── registro.html
│       ├── perfil.html
│       ├── carrito.html
│       ├── checkout.html
│       ├── mis_tarjetas.html
│       └── completar_perfil.html
├── administradores/          # App de administración
│   ├── models.py             # Administrador
│   ├── views.py              # panel, CRUD, reportes, perfil
│   └── templates/administradores/
│       ├── panel.html        # Dashboard con KPIs y Chart.js
│       ├── listar_productos.html
│       ├── crear_producto.html
│       ├── editar_producto.html
│       ├── listar_categorias.html
│       ├── listar_usuarios.html
│       ├── ventas_dia.html
│       ├── ventas_reporte.html
│       ├── detalle_venta.html
│       └── perfil.html
├── api/                      # REST API (Django REST Framework)
│   ├── views.py
│   ├── serializers.py
│   ├── authentication.py
│   └── urls.py
├── ventas/                   # Modelo de ventas
│   └── models.py             # Venta, ItemVenta
├── media/                    # Imágenes subidas (productos, categorías)
├── requirements.txt
└── manage.py
```

---

## Comandos Útiles

```bash
# Cargar datos iniciales
python manage.py cargar_datos

# Recargar datos (limpia primero)
python manage.py cargar_datos --clear

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recolectar estáticos (producción)
python manage.py collectstatic

# Shell de Django
python manage.py shell

# Servidor en otro puerto
python manage.py runserver 8001
```

---

## Tecnologías

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| Python | 3.14 | Lenguaje principal |
| Django | 6.0.4 | Framework web |
| PostgreSQL | 16+ | Base de datos |
| Django REST Framework | 3.17.1 | API REST |
| psycopg2-binary | 2.9.12 | Adaptador PostgreSQL |
| Pillow | 12.2.0 | Imágenes de productos |
| PyJWT | 2.12.1 | Tokens JWT para API |
| requests | 2.33.1 | Google OAuth / HTTP |
| Bootstrap | 5.3 | UI (servido localmente) |
| Font Awesome | 6 | Íconos (servido localmente) |
| Chart.js | 4.4.3 | Gráficas en panel admin |
