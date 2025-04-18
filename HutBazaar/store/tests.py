from django.test import TestCase
from django.urls import reverse
from store.models.product import Product
from store.models.category import Category


class HomePageViewTest(TestCase):
    def setUp(self):
        # Set up a test category and product
        self.category = Category.objects.create(name='Oil')
        self.product = Product.objects.create(
            name='Rupchanda Oil',
            price=800,
            category=self.category,
            description='5L Rupchanda Oil',
            image='products/Rupchanda Soyabean oil.jpg'
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_contains_product(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Rupchanda Oil')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Oil')
        self.product = Product.objects.create(
            name='Rupchanda Oil',
            price=800,
            category=self.category,
            description='5L Rupchanda Oil',
            image='products/Rupchanda Soyabean oil.jpg'
        )

    def test_product_detail_view(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rupchanda Oil')

