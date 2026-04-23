from django.core.management.base import BaseCommand
from catalogo.models import Categoria, Producto
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga los datos iniciales de categorías y productos para mayoreo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpia los datos existentes antes de cargar nuevos datos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            Producto.objects.all().delete()
            Categoria.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Datos existentes eliminados.'))

        # Datos de categorías y productos
        datos = {
            ('🥤 Refrescos y Bebidas Carbonatadas', '🥤'): [
                ('Coca-Cola', '600ml', 'Coca-Cola', 'Paquete', 12, Decimal('32.00')),
                ('Coca-Cola', 'Lata 355ml', 'Coca-Cola', 'Paquete', 12, Decimal('35.00')),
                ('Coca-Cola', '1.5L', 'Coca-Cola', 'Paquete', 6, Decimal('40.00')),
                ('Coca-Cola', '3L', 'Coca-Cola', 'Paquete', 8, Decimal('60.00')),
                ('Pepsi', '600ml', 'Pepsi', 'Paquete', 12, Decimal('30.00')),
                ('Pepsi', 'Lata 355ml', 'Pepsi', 'Paquete', 12, Decimal('32.00')),
                ('Pepsi', '2L', 'Pepsi', 'Paquete', 6, Decimal('38.00')),
                ('Sprite', '600ml', 'Sprite', 'Paquete', 12, Decimal('32.00')),
                ('Sprite', 'Lata 355ml', 'Sprite', 'Paquete', 12, Decimal('35.00')),
                ('Fanta Naranja', '600ml', 'Fanta', 'Paquete', 12, Decimal('30.00')),
                ('Fanta Naranja', 'Lata 355ml', 'Fanta', 'Paquete', 12, Decimal('32.00')),
                ('Mundet Manzana', '600ml', 'Mundet', 'Paquete', 12, Decimal('28.00')),
                ('Peñafiel Toronja', '600ml', 'Peñafiel', 'Paquete', 12, Decimal('28.00')),
                ('Peñafiel Toronja', 'Lata 355ml', 'Peñafiel', 'Paquete', 12, Decimal('30.00')),
            ],
            ('💧 Aguas y Bebidas Sin Gas', '💧'): [
                ('Agua Ciel', '600ml', 'Ciel', 'Paquete', 12, Decimal('18.00')),
                ('Agua Ciel', '1.5L', 'Ciel', 'Paquete', 6, Decimal('22.00')),
                ('Agua Ciel', '5L', 'Ciel', 'Paquete', 4, Decimal('28.00')),
                ('Agua E-Pura', '600ml', 'E-Pura', 'Paquete', 12, Decimal('18.00')),
                ('Agua E-Pura', '1.5L', 'E-Pura', 'Paquete', 6, Decimal('22.00')),
                ('Agua Mineral Peñafiel', '500ml', 'Peñafiel', 'Paquete', 12, Decimal('20.00')),
                ('Agua Mineral Peñafiel', 'Lata 355ml', 'Peñafiel', 'Paquete', 12, Decimal('18.00')),
                ('Gatorade', 'Limón 600ml', 'Gatorade', 'Paquete', 12, Decimal('42.00')),
                ('Gatorade', 'Naranja 600ml', 'Gatorade', 'Paquete', 12, Decimal('42.00')),
                ('Powerade', 'Uva 600ml', 'Powerade', 'Paquete', 12, Decimal('40.00')),
            ],
            ('🧃 Jugos y Néctares', '🧃'): [
                ('Jugo Del Valle', 'Naranja 335ml', 'Del Valle', 'Paquete', 12, Decimal('28.00')),
                ('Jugo Del Valle', 'Naranja 1L', 'Del Valle', 'Paquete', 12, Decimal('38.00')),
                ('Jugo Del Valle', 'Durazno 335ml', 'Del Valle', 'Paquete', 12, Decimal('28.00')),
                ('Jumex Mango', 'Lata 355ml', 'Jumex', 'Paquete', 24, Decimal('48.00')),
                ('Jumex Naranja', 'Lata 355ml', 'Jumex', 'Paquete', 24, Decimal('48.00')),
                ('Jumex Guayaba', '500ml', 'Jumex', 'Paquete', 12, Decimal('35.00')),
                ('V8 Original', '250ml', 'V8', 'Paquete', 12, Decimal('42.00')),
            ],
            ('☕ Bebidas Calientes y Lácteas', '☕'): [
                ('Café Nescafé', 'Clásico 200g', 'Nescafé', 'Caja', 12, Decimal('180.00')),
                ('Café Nescafé', 'Clásico 400g', 'Nescafé', 'Caja', 6, Decimal('280.00')),
                ('Chocolate Abuelita', '540g', 'Abuelita', 'Caja', 12, Decimal('150.00')),
                ('Leche Lala', 'Entera 1L', 'Lala', 'Paquete', 12, Decimal('36.00')),
                ('Leche Lala', 'Entera 2L', 'Lala', 'Paquete', 6, Decimal('58.00')),
                ('Leche en Polvo Nido', '1.1kg', 'Nido', 'Caja', 6, Decimal('320.00')),
                ('Leche en Polvo Nido', '400g', 'Nido', 'Caja', 12, Decimal('140.00')),
            ],
            ('🍚 Granos y Cereales', '🍚'): [
                ('Arroz Morelos', '1kg', 'Morelos', 'Bulto', 10, Decimal('85.00')),
                ('Arroz Morelos', '5kg', 'Morelos', 'Bulto', 4, Decimal('380.00')),
                ('Arroz Morelos', '10kg', 'Morelos', 'Costal', 1, Decimal('720.00')),
                ('Frijol Negro', '1kg', 'Morelos', 'Bulto', 10, Decimal('95.00')),
                ('Frijol Negro', '5kg', 'Morelos', 'Bulto', 4, Decimal('420.00')),
                ('Frijol Bayo', '1kg', 'Morelos', 'Bulto', 10, Decimal('85.00')),
                ('Frijol Bayo', '10kg', 'Morelos', 'Costal', 1, Decimal('780.00')),
                ('Lenteja', '500g', 'Genérica', 'Caja', 20, Decimal('65.00')),
                ('Avena Quaker', '500g', 'Quaker', 'Caja', 12, Decimal('48.00')),
                ('Avena Quaker', '1kg', 'Quaker', 'Caja', 6, Decimal('85.00')),
                ('Maíz Pozolero', '1kg', 'Genérica', 'Bulto', 10, Decimal('45.00')),
            ],
            ('🍝 Pastas y Sopas', '🍝'): [
                ('Fideo La Moderna', '200g', 'La Moderna', 'Caja', 20, Decimal('40.00')),
                ('Fideo La Moderna', '500g', 'La Moderna', 'Caja', 12, Decimal('65.00')),
                ('Espagueti Barilla', '400g', 'Barilla', 'Caja', 12, Decimal('85.00')),
                ('Espagueti Barilla', '900g', 'Barilla', 'Caja', 6, Decimal('155.00')),
                ('Sopa Estrellitas La Moderna', '200g', 'La Moderna', 'Caja', 20, Decimal('35.00')),
                ('Maruchan', 'Vaso 64g', 'Maruchan', 'Caja', 24, Decimal('48.00')),
                ('Maruchan', 'Sobre 85g', 'Maruchan', 'Caja', 24, Decimal('58.00')),
                ('Caldo de Pollo Knorr', '100g', 'Knorr', 'Caja', 24, Decimal('65.00')),
                ('Caldo de Pollo Knorr', '400g', 'Knorr', 'Caja', 12, Decimal('145.00')),
            ],
            ('🥫 Enlatados y Conservas', '🥫'): [
                ('Atún Herdez', 'En Agua 140g', 'Herdez', 'Caja', 24, Decimal('135.00')),
                ('Atún Herdez', 'En Aceite 140g', 'Herdez', 'Caja', 24, Decimal('145.00')),
                ('Sardina Cumbres', 'En Tomate 425g', 'Cumbres', 'Caja', 24, Decimal('185.00')),
                ('Frijoles Herdez', '400g', 'Herdez', 'Caja', 24, Decimal('95.00')),
                ('Chiles en Vinagre La Morena', '380g', 'La Morena', 'Caja', 12, Decimal('95.00')),
                ('Chiles en Vinagre La Morena', '800g', 'La Morena', 'Caja', 6, Decimal('165.00')),
                ('Duraznos Del Monte', 'En Almíbar 820g', 'Del Monte', 'Caja', 12, Decimal('125.00')),
            ],
            ('🧂 Aceites, Salsas y Condimentos', '🧂'): [
                ('Aceite Nutrioli', '1L', 'Nutrioli', 'Caja', 12, Decimal('180.00')),
                ('Aceite Nutrioli', '3L', 'Nutrioli', 'Caja', 4, Decimal('475.00')),
                ('Aceite de Oliva Carbonell', '750ml', 'Carbonell', 'Caja', 6, Decimal('280.00')),
                ('Salsa Valentina', '370ml', 'Valentina', 'Caja', 12, Decimal('85.00')),
                ('Salsa Valentina', '1L', 'Valentina', 'Caja', 6, Decimal('185.00')),
                ('Salsa Maggi', '250ml', 'Maggi', 'Caja', 12, Decimal('95.00')),
                ('Mayonesa McCormick', '390g', 'McCormick', 'Caja', 12, Decimal('125.00')),
                ('Mayonesa McCormick', '1kg', 'McCormick', 'Caja', 6, Decimal('265.00')),
                ('Vinagre Ybarra', '500ml', 'Ybarra', 'Caja', 12, Decimal('105.00')),
            ],
            ('🍬 Dulces y Botanas', '🍬'): [
                ('Sabritas Clásicas', '45g', 'Sabritas', 'Caja', 10, Decimal('55.00')),
                ('Sabritas Clásicas', '130g', 'Sabritas', 'Caja', 10, Decimal('125.00')),
                ('Ruffles Queso', '45g', 'Ruffles', 'Caja', 10, Decimal('55.00')),
                ('Ruffles Queso', '130g', 'Ruffles', 'Caja', 10, Decimal('125.00')),
                ('Gomitas Ricolino', '65g', 'Ricolino', 'Caja', 24, Decimal('95.00')),
                ('Mazapán De la Rosa', '30g', 'De la Rosa', 'Caja', 30, Decimal('120.00')),
                ('Paletas Payaso', '30g', 'Payaso', 'Caja', 24, Decimal('85.00')),
                ('Chicles Clorets', '12 pzs', 'Clorets', 'Caja', 24, Decimal('75.00')),
            ],
            ('🧻 Limpieza del Hogar', '🧻'): [
                ('Papel Higiénico Regio', '180 hojas', 'Regio', 'Paquete', 12, Decimal('65.00')),
                ('Papel Higiénico Regio', '360 hojas', 'Regio', 'Paquete', 6, Decimal('85.00')),
                ('Servilletas Kleenex', '250 pzs', 'Kleenex', 'Paquete', 12, Decimal('85.00')),
                ('Detergente Ariel', '1kg', 'Ariel', 'Caja', 10, Decimal('145.00')),
                ('Detergente Ariel', '3kg', 'Ariel', 'Caja', 4, Decimal('385.00')),
                ('Cloro Cloralex', '1L', 'Cloralex', 'Caja', 12, Decimal('55.00')),
                ('Cloro Cloralex', '4L', 'Cloralex', 'Caja', 4, Decimal('125.00')),
                ('Fabuloso Multiusos', '1L', 'Fabuloso', 'Caja', 12, Decimal('65.00')),
                ('Fabuloso Multiusos', '5L', 'Fabuloso', 'Caja', 4, Decimal('235.00')),
                ('Jabón Roma', '250g', 'Roma', 'Caja', 20, Decimal('95.00')),
            ],
            ('🧼 Higiene Personal', '🧼'): [
                ('Jabón Palmolive', '150g', 'Palmolive', 'Caja', 24, Decimal('125.00')),
                ('Jabón Palmolive', '400g', 'Palmolive', 'Caja', 12, Decimal('185.00')),
                ('Shampoo Pantene', '400ml', 'Pantene', 'Caja', 12, Decimal('165.00')),
                ('Shampoo Pantene', '750ml', 'Pantene', 'Caja', 6, Decimal('265.00')),
                ('Pasta Dental Colgate', '100ml', 'Colgate', 'Caja', 12, Decimal('95.00')),
                ('Pasta Dental Colgate', '200ml', 'Colgate', 'Caja', 6, Decimal('155.00')),
                ('Desodorante Dove', '150ml', 'Dove', 'Caja', 12, Decimal('185.00')),
            ],
            ('🍞 Panadería y Snacks Empacados', '🍞'): [
                ('Gansito Marinela', '42g', 'Marinela', 'Caja', 24, Decimal('125.00')),
                ('Pingüinos Marinela', '39g', 'Marinela', 'Caja', 24, Decimal('120.00')),
                ('Galletas Marías Gamesa', '200g', 'Gamesa', 'Caja', 12, Decimal('85.00')),
                ('Galletas Marías Gamesa', '500g', 'Gamesa', 'Caja', 6, Decimal('155.00')),
                ('Pan Bimbo Blanco', '680g', 'Bimbo', 'Paquete', 6, Decimal('95.00')),
                ('Obleas con Cajeta', '30g', 'Genérica', 'Caja', 50, Decimal('185.00')),
            ],
        }

        # Cargar datos
        total_productos = 0
        for (cat_nombre, emoji), productos_lista in datos.items():
            categoria, _ = Categoria.objects.get_or_create(
                nombre=cat_nombre,
                defaults={
                    'icono_emoji': emoji,
                    'descripcion': f'Productos de {cat_nombre}'
                }
            )
            self.stdout.write(f'Categoría creada/actualizada: {cat_nombre}')

            for nombre, gramaje, marca, tipo_paquete, piezas, precio in productos_lista:
                producto, created = Producto.objects.get_or_create(
                    nombre=nombre,
                    gramaje=gramaje,
                    categoria=categoria,
                    defaults={
                        'marca': marca,
                        'tipo_paquete': tipo_paquete,
                        'piezas_por_paquete': piezas,
                        'precio': precio,
                        'stock': 50,  # Stock inicial
                        'activo': True
                    }
                )
                if created:
                    total_productos += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Carga de datos completada exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'✓ {Categoria.objects.count()} categorías cargadas'))
        self.stdout.write(self.style.SUCCESS(f'✓ {total_productos} nuevos productos cargados'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total de productos: {Producto.objects.count()}'))
