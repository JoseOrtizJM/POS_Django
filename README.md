# 🛍️ POS Django - Sistema de Punto de Venta Mayoreo

> **Sistema completo de Punto de Venta (POS)** para gestión de mayoreo de abarrotes con autenticación, roles de usuario, panel de administración y CRUD de productos.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-6.0+-darkgreen?style=flat-square)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura](#estructura)
- [Autenticación](#autenticación)
- [Panel de Administración](#panel-de-administración)
- [Diseño y Estilos](#diseño-y-estilos)
- [Comandos Útiles](#comandos-útiles)

---

## ✨ Características

### 🔐 Sistema de Autenticación Completo
- **Login**: Ingreso con email y contraseña
- **Registro**: Creación de nuevas cuentas con validaciones
- **Validación de Email**: Verificación de formato automática
- **Roles**: Admin y Usuario Regular

### 👥 Gestión de Usuarios
- Dos tipos de roles:
  - **Administrador**: Acceso total a gestión
  - **Usuario Regular**: Acceso solo a catálogo
- Vista de usuarios registrados (solo admin)
- Estadísticas de usuarios

### 🛒 Catálogo de Productos
- **8 Categorías** precargadas con emoji
- **26 Productos** de ejemplo listos para usar
- Interfaz responsive con diseño oscuro profesional
- Búsqueda y filtrado de productos
- Visualización de:
  - Nombre y marca
  - Gramaje/presentación
  - Precio en $MXN
  - Stock disponible
  - Descripción del producto

### ⚙️ Panel de Administración
- **Dashboard Admin** con estadísticas
- **CRUD Completo de Productos**:
  - ✅ Crear nuevos productos
  - ✅ Editar productos existentes
  - ✅ Eliminar productos
  - ✅ Ver lista de productos
- **Gestión de Usuarios**:
  - Ver lista de usuarios
  - Ver rol de cada usuario
  - Ver fecha de registro
  - Búsqueda en tiempo real

### 🎨 Diseño y Estilos
- **CSS Separado** en archivos estáticos
- **JavaScript Separado** en archivos estáticos
- Tema oscuro personalizado
- Animaciones suaves
- Interfaz 100% responsive
- Compatibilidad móvil garantizada

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes de Python)
- Git (opcional)

### Pasos

1. **Clonar o descargar el proyecto**
   ```bash
   cd "c:\Users\joseo\OneDrive\Documentos\S8\Web\Django-Final"
   ```

2. **Crear ambiente virtual (si es necesario)**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Cargar datos iniciales**
   ```bash
   python manage.py cargar_datos
   ```

6. **Crear usuario administrador (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```

8. **Acceder a la aplicación**
   - Dashboard: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/panel/
   - Django Admin: http://localhost:8000/admin/

---

## 🔑 Uso

### Flujo de Uso

#### Como Usuario Regular
1. Ir a http://localhost:8000/
2. Hacer clic en "Registrarse"
3. Crear cuenta con email y contraseña
4. Ver catálogo de productos
5. Seleccionar categoría para ver productos

#### Como Administrador
1. Iniciar sesión con cuenta admin
2. Ir a http://localhost:8000/admin/panel/
3. Acciones disponibles:
   - ➕ Crear nuevos productos
   - ✏️ Editar productos
   - 🗑️ Eliminar productos
   - 👥 Ver usuarios registrados

---

## 📁 Estructura del Proyecto

```
Django-Final/
├── catalogo/
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_usuariopos.py          ← Nuevo modelo
│   ├── management/
│   │   └── commands/
│   │       └── cargar_datos.py         ← Script de datos
│   ├── static/                          ← ✅ Archivos estáticos
│   │   └── catalogo/
│   │       ├── css/
│   │       │   └── style.css           ← ✅ CSS separado
│   │       └── js/
│   │           └── main.js             ← ✅ JS separado
│   ├── templates/                       ← Templates HTML
│   │   └── catalogo/
│   │       ├── base.html               ← Template base
│   │       ├── login.html              ← ✅ Login
│   │       ├── registro.html           ← ✅ Registro
│   │       ├── dashboard.html          ← Dashboard
│   │       ├── productos_categoria.html
│   │       ├── admin_panel.html        ← ✅ Panel admin
│   │       ├── crear_producto.html     ← ✅ Crear
│   │       ├── editar_producto.html    ← ✅ Editar
│   │       └── listar_usuarios.html    ← ✅ Ver usuarios
│   ├── models.py                        ← ✅ Nuevo modelo UsuarioPOS
│   ├── views.py                         ← ✅ Nuevas vistas
│   ├── urls.py                          ← ✅ Nuevas rutas
│   ├── forms.py                         ← ✅ Nuevos formularios
│   ├── admin.py
│   └── apps.py
├── POS_Django/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3                           ← Base de datos
├── INSTRUCCIONES.txt                    ← Instrucciones completas
└── README.md                            ← Este archivo
```

---

## 🔐 Autenticación

### Página de Login
- **URL**: http://localhost:8000/login/
- **Campos**: Email, Contraseña
- **Validaciones**: 
  - Email válido
  - Contraseña requerida
  - Usuario existe en BD

### Página de Registro
- **URL**: http://localhost:8000/registro/
- **Campos**: 
  - Correo electrónico
  - Contraseña (mínimo 8 caracteres)
  - Confirmación de contraseña
- **Validaciones**:
  - Email válido y único
  - Formato de email correcto
  - Contraseñas coinciden
  - Contraseña mínimo 8 caracteres

### Cierre de Sesión
- Botón en navbar: "Cerrar Sesión"
- Elimina sesión del usuario

---

## 🎛️ Panel de Administración

### Acceso
- **URL**: http://localhost:8000/admin/panel/
- **Restricción**: Solo administradores
- **Redirección**: Si no eres admin, te redirecciona

### Dashboard
Muestra estadísticas en tiempo real:
- Total de productos
- Total de usuarios
- Total de categorías
- Últimos 5 productos

### Gestión de Productos

#### ➕ Crear Producto
- **URL**: http://localhost:8000/admin/crear-producto/
- **Campos**:
  - Nombre ⭐
  - Marca ⭐
  - Gramaje ⭐
  - Categoría ⭐
  - Tipo de Paquete ⭐
  - Piezas por Paquete ⭐
  - Precio ($) ⭐
  - Stock ⭐
  - Imagen (opcional)
  - Descripción (opcional)
- ⭐ = Campos requeridos

#### ✏️ Editar Producto
- Acceso desde tabla del dashboard admin
- Permite modificar todos los campos
- Validaciones automáticas

#### 🗑️ Eliminar Producto
- Confirmación de seguridad
- Eliminación irreversible
- Actualización instantánea

### Gestión de Usuarios
- **URL**: http://localhost:8000/admin/usuarios/
- **Información mostrada**:
  - Email
  - Usuario
  - Rol (Admin/Usuario)
  - Estado (Activo/Inactivo)
  - Fecha de registro
- **Búsqueda en tiempo real** ⚡

---

## 🎨 Diseño y Estilos

### Tema
- **Color Primario**: Azul oscuro (#130961)
- **Color Secundario**: Verde (#10b981)
- **Fondo**: Gris oscuro (#3b3b3b)
- **Texto Principal**: Gris claro (#e0e0e0)

### Archivos Estáticos
Todos los estilos y scripts están **separados en archivos externos**:

```
catalogo/static/catalogo/
├── css/
│   └── style.css      (Todos los estilos)
└── js/
    └── main.js        (Todas las funciones)
```

### Características CSS
- Variables CSS para temas
- Animaciones suaves
- Responsive design
- Compatibilidad con Bootstrap 5

### Funciones JavaScript
- Validaciones
- Búsqueda en tablas
- Notificaciones toast
- Utilidades generales

---

## 🔄 Comandos Útiles

### Cargar/Recargar Datos
```bash
# Primera vez o para agregar datos
python manage.py cargar_datos

# Limpiar y recargar todo
python manage.py cargar_datos --clear
```

### Migraciones
```bash
# Ver cambios sin aplicar
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver historial
python manage.py migrate --list
```

### Usuario Admin
```bash
# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña
python manage.py changepassword <username>
```

### Utilidades
```bash
# Activar shell de Django
python manage.py shell

# Recolectar archivos estáticos (producción)
python manage.py collectstatic

# Crear aplicación nueva
python manage.py startapp <app_name>
```

---

## 📊 Datos Cargados

### Categorías (8)
1. 🫒 Aceites y Grasas
2. 🥤 Bebidas
3. 🌾 Alimentos Secos
4. 🧀 Productos Lácteos
5. 🥩 Carnes y Embutidos
6. 🍯 Salsas y Condimentos
7. 🥫 Conservas
8. 🥨 Snacks

### Productos (26)
Incluye productos de ejemplo como:
- Aceite de Oliva Extra Virgen
- Refrescos y Bebidas
- Arroz, Frijoles, Pasta
- Leche y Productos Lácteos
- Jamón, Salchicha, Tocino
- Salsa de Tomate, Mayonesa
- Atún en Lata, Chícharos
- Papas Fritas, Cacahuates

---

## 🌐 URLs Disponibles

### Públicas (sin login requerido)
- `/login/` - Página de inicio de sesión
- `/registro/` - Página de registro

### De Usuario
- `/` - Dashboard/Inicio
- `/categoria/<id>/` - Productos por categoría
- `/logout/` - Cerrar sesión

### De Administrador
- `/admin/panel/` - Panel de administración
- `/admin/crear-producto/` - Crear producto
- `/admin/editar-producto/<id>/` - Editar producto
- `/admin/eliminar-producto/<id>/` - Eliminar producto
- `/admin/usuarios/` - Ver usuarios

### Django Admin
- `/admin/` - Panel de administración de Django

---

## ⚡ Rendimiento

- Base de datos SQLite (desarrollo)
- Carga inicial de datos: < 2 segundos
- Búsqueda en tablas: Instantánea
- Interfaz responsive: Optimizada

---

## 🐛 Solución de Problemas

### Puerto 8000 ocupado
```bash
python manage.py runserver 8001
```

### Base de datos corrupta
```bash
# Eliminar db.sqlite3 y recrear
python manage.py migrate
python manage.py cargar_datos
```

### Archivos estáticos no se cargan
```bash
python manage.py collectstatic
```

### Error de migraciones
```bash
python manage.py migrate catalogo zero
python manage.py migrate
```

---

## 📝 Licencia

Este proyecto está bajo licencia MIT.

---

## 🙏 Créditos

Desarrollado con:
- Django 6.0.4
- Bootstrap 5.3
- Font Awesome 6.4
- Python 3.8+

---

## 📞 Soporte

Para preguntas o problemas, consulta el archivo **INSTRUCCIONES.txt** para una guía completa.

---

**Última actualización**: 28 de Abril, 2026  
**Versión**: 2.0 (Con autenticación y panel admin)

Se importaron **12 categorías** con sus emojis representativos:

1. 🥤 Refrescos y Bebidas Carbonatadas (14 productos)
2. 💧 Aguas y Bebidas Sin Gas (10 productos)
3. 🧃 Jugos y Néctares (7 productos)
4. ☕ Bebidas Calientes y Lácteas (7 productos)
5. 🍚 Granos y Cereales (11 productos)
6. 🍝 Pastas y Sopas (9 productos)
7. 🥫 Enlatados y Conservas (7 productos)
8. 🧂 Aceites, Salsas y Condimentos (9 productos)
9. 🍬 Dulces y Botanas (8 productos)
10. 🧻 Limpieza del Hogar (10 productos)
11. 🧼 Higiene Personal (7 productos)
12. 🍞 Panadería y Snacks Empacados (6 productos)

**Total: 105 productos cargados**

### 4. **Modelos de Datos** 🗄️

#### Categoria
- `nombre`: Nombre único de la categoría
- `descripcion`: Descripción opcional
- `icono_emoji`: Emoji representativo (ej: 🥤)
- `imagen`: Opcional para imagen de categoría
- Timestamps: `creado_en`, `actualizado_en`

#### Producto
- `nombre`: Nombre del producto
- `marca`: Marca del producto
- `gramaje`: Presentación (600ml, 1kg, 250g, etc.)
- `categoria`: ForeignKey a Categoría
- `tipo_paquete`: Paquete, Caja, Bulto, Costal
- `piezas_por_paquete`: Cantidad de unidades por paquete
- `precio`: Precio en pesos mexicanos (DecimalField)
- `stock`: Inventario en paquetes
- `descripcion`: Descripción adicional
- `imagen`: Campo para imagen del producto
- `activo`: Estado del producto
- Timestamps: `creado_en`, `actualizado_en`

### 5. **Panel de Administración** 🔐
- Acceso completo a gestión de categorías y productos
- Interfaz personalizada con campos organizados
- Filtros y búsqueda integrados
- Readonly de campos de fecha

---

## Estructura del Proyecto

```
Django-Final/
├── manage.py
├── db.sqlite3
├── POS_Django/
│   ├── settings.py (actualizado)
│   ├── urls.py (actualizado)
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
├── catalogo/
│   ├── models.py (Categoria, Producto)
│   ├── admin.py (registro en admin)
│   ├── views.py (dashboard, productos_por_categoria)
│   ├── urls.py (rutas)
│   ├── management/
│   │   └── commands/
│   │       └── cargar_datos.py (comando para cargar datos)
│   └── templates/
│       └── catalogo/
│           ├── base.html (template base)
│           ├── dashboard.html (listado de categorías)
│           └── productos_categoria.html (listado de productos)
├── media/ (archivos multimedia)
├── staticfiles/ (archivos estáticos)
└── venv/ (entorno virtual)
```

---

## Cómo Usar

### 1. **Iniciar el servidor**
```bash
cd "c:\Users\joseo\OneDrive\Documentos\S8\Web\Django-Final"
python manage.py runserver
```

### 2. **Acceder a la aplicación**
- **Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
  - Usuario: `admin`
  - Contraseña: `admin123`

### 3. **Cargar más datos**
```bash
python manage.py cargar_datos --clear  # Limpia datos existentes e importa nuevos
```

### 4. **Crear migraciones (si modificas los modelos)**
```bash
python manage.py makemigrations catalogo
python manage.py migrate
```

---

## Personalización y Próximos Pasos

### Sugerencias para expansión:
1. **Carrito de compras**: Agregar funcionalidad de compra
2. **Descuentos**: Sistema de promociones por volumen
3. **Reportes**: Generación de reportes de ventas
4. **Usuarios**: Sistema de login para clientes
5. **Búsqueda y filtros**: Buscador de productos avanzado
6. **Imágenes de categorías**: Subir imágenes en lugar de emojis
7. **PDF**: Generación de boletas de compra
8. **API REST**: Crear endpoints para aplicaciones móviles

---

## Tecnologías Utilizadas

- **Backend**: Django 4.2.27
- **Frontend**: Bootstrap 5.3.0
- **Base de Datos**: SQLite3
- **CSS/JS**: Customizado + Font Awesome 6.4.0

---

## Notas Importantes

✅ Todos los precios están en **Pesos Mexicanos ($)**
✅ Los emojis se muestran automáticamente en cada categoría
✅ El sistema es completamente responsive
✅ Los estilos CSS incluyen animaciones suaves y hover effects
✅ La tabla de productos es ordenable y sorteable
✅ Stock con indicadores visuales de disponibilidad

---

**Proyecto completado exitosamente el 22 de abril de 2026** 🎉
