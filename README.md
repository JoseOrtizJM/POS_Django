# POS Django - Punto de Venta Mayoreo ✅

## Descripción General
Sistema completo de Punto de Venta (POS) para gestión de mayoreo de abarrotes, con categorías de productos, dashboard interactivo y visualización detallada de productos.

---

## Características Implementadas

### 1. **Dashboard Principal** 🏠
- Página de inicio con todas las categorías dispuestas en cuadrados/tarjetas
- Diseño responsive con animaciones suaves
- Cada tarjeta contiene:
  - Emoji representativo de la categoría
  - Nombre de la categoría
  - Cantidad de productos disponibles
  - Navegación directa al hacer clic

### 2. **Página de Productos por Categoría** 📋
- Tabla completa con información de todos los productos
- Detalles mostrados:
  - **Nombre y Marca** del producto
  - **Presentación** (gramaje: 600ml, 1kg, etc.)
  - **Tipo de Paquete** (Paquete, Caja, Bulto, Costal)
  - **Cantidad de piezas** por paquete
  - **Precio** en pesos mexicanos 🇲🇽
  - **Stock** disponible con indicadores visuales
- Breadcrumb de navegación para volver al dashboard

### 3. **Categorías Cargadas** 📦
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
