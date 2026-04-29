from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from administradores.models import Administrador


class Command(BaseCommand):
    help = 'Carga un administrador y dos clientes de prueba con datos realistas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los usuarios y administradores antes de cargar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando usuarios y administradores existentes...'))
            Usuario.objects.all().delete()
            Administrador.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Datos eliminados.'))

        # ==================== ADMINISTRADOR ====================
        self.stdout.write(self.style.HTTP_INFO('\nCreando administrador...'))

        admin_data = {
            'email': 'admin@mayoreopos.mx',
            'nombre_usuario': 'admin_pos',
            'password': 'Admin1234',
        }

        if Administrador.objects.filter(email=admin_data['email']).exists():
            self.stdout.write(f"  ℹ Administrador '{admin_data['nombre_usuario']}' ya existe, se omite.")
        else:
            admin = Administrador(
                email=admin_data['email'],
                nombre_usuario=admin_data['nombre_usuario'],
                activo=True,
            )
            admin.set_password(admin_data['password'])
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                f"  ✓ Administrador '{admin.nombre_usuario}' creado  —  correo: {admin.email}  |  contraseña: {admin_data['password']}"
            ))

        # ==================== CLIENTES ====================
        self.stdout.write(self.style.HTTP_INFO('\nCreando clientes...'))

        clientes_data = [
            {
                'email': 'maria.garcia@gmail.com',
                'nombre_usuario': 'mariag',
                'password': 'Cliente123',
                'nombre_completo': 'María García López',
                'telefono': '5512345678',
                'direccion': 'Av. Insurgentes Sur 1602, Col. Crédito Constructor',
                'ciudad': 'Ciudad de México',
                'estado_provincia': 'CDMX',
                'codigo_postal': '03940',
                'pais': 'MX',
            },
            {
                'email': 'carlos.mendez@hotmail.com',
                'nombre_usuario': 'carlosm',
                'password': 'Cliente123',
                'nombre_completo': 'Carlos Méndez Rojas',
                'telefono': '3312345678',
                'direccion': 'Calle Juárez 456, Col. Centro Histórico',
                'ciudad': 'Guadalajara',
                'estado_provincia': 'Jalisco',
                'codigo_postal': '44100',
                'pais': 'MX',
            },
        ]

        for data in clientes_data:
            if Usuario.objects.filter(email=data['email']).exists():
                self.stdout.write(f"  ℹ Cliente '{data['nombre_usuario']}' ya existe, se omite.")
                continue

            usuario = Usuario(
                email=data['email'],
                nombre_usuario=data['nombre_usuario'],
                nombre_completo=data['nombre_completo'],
                telefono=data['telefono'],
                direccion=data['direccion'],
                ciudad=data['ciudad'],
                estado_provincia=data['estado_provincia'],
                codigo_postal=data['codigo_postal'],
                pais=data['pais'],
                activo=True,
            )
            usuario.set_password(data['password'])
            usuario.save()
            self.stdout.write(self.style.SUCCESS(
                f"  ✓ Cliente '{usuario.nombre_usuario}' creado  —  correo: {usuario.email}  |  contraseña: {data['password']}"
            ))

        # ==================== RESUMEN ====================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Total administradores: {Administrador.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Total clientes:        {Usuario.objects.count()}'))
        self.stdout.write('')
        self.stdout.write('Credenciales de acceso:')
        self.stdout.write('  Admin   →  /administradores/login/  |  usuario: admin_pos  |  contraseña: Admin1234')
        self.stdout.write('  Cliente →  /usuarios/login/         |  usuario: mariag     |  contraseña: Cliente123')
        self.stdout.write('  Cliente →  /usuarios/login/         |  usuario: carlosm    |  contraseña: Cliente123')
