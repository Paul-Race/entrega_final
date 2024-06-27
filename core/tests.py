from django.contrib.auth.models import User
from django.test import TestCase
from .models import Tecnica, Obra, CarritoCompras

class TecnicaModelTest(TestCase):
    def setUp(self):
        self.tecnica = Tecnica.objects.create(descripcion='Técnica de prueba')

    def test_tecnica_crud(self):
        # Read
        self.assertEqual(self.tecnica.descripcion, 'Técnica de prueba')

        # Update
        self.tecnica.descripcion = 'Técnica actualizada'
        self.tecnica.save()
        self.assertEqual(self.tecnica.descripcion, 'Técnica actualizada')

        # Delete
        self.tecnica.delete()
        self.assertEqual(Tecnica.objects.count(), 0)

class ObraModelTest(TestCase):
    def setUp(self):
        self.tecnica = Tecnica.objects.create(descripcion='Técnica de prueba')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.obra = Obra.objects.create(
            titulo='Obra de prueba',
            descripcion='Esta es una obra de prueba',
            historia='Esta es la historia de la obra de prueba',
            precio=1000,
            tecnica=self.tecnica,
            colaborador=self.user
        )

    def test_obra_crud(self):
        # Read
        self.assertEqual(self.obra.titulo, 'Obra de prueba')

        # Update
        self.obra.titulo = 'Obra actualizada'
        self.obra.save()
        self.assertEqual(self.obra.titulo, 'Obra actualizada')

        # Delete
        self.obra.delete()
        self.assertEqual(Obra.objects.count(), 0)

class CarritoComprasModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.carrito = CarritoCompras.objects.create(cliente=self.user)

    def test_carrito_crud(self):
        # Read
        self.assertEqual(self.carrito.cliente, self.user)

        # Update
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.carrito.cliente = self.user2
        self.carrito.save()
        self.assertEqual(self.carrito.cliente, self.user2)

        # Delete
        self.carrito.delete()
        self.assertEqual(CarritoCompras.objects.count(), 0)


class CarritoComprasTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create some artworks
        self.obra1 = Obra.objects.create(titulo='Obra 1', precio=100, colaborador=self.user)
        self.obra2 = Obra.objects.create(titulo='Obra 2', precio=200, colaborador=self.user)

    def test_agregar_obras(self):
        # Create a cart for the user
        carrito = CarritoCompras.objects.create(cliente=self.user)
        carrito.obras.add(self.obra1, self.obra2)

        # Check if the artworks were added
        self.assertEqual(carrito.obras.count(), 2)
        self.assertEqual(list(carrito.obras.all()), [self.obra1, self.obra2])

    def test_vaciar_carrito(self):
        # Create a cart for the user and add some artworks
        carrito = CarritoCompras.objects.create(cliente=self.user)
        carrito.obras.add(self.obra1, self.obra2)

        # Empty the cart
        carrito.obras.clear()

        # Check if the cart is empty
        self.assertEqual(carrito.obras.count(), 0)
