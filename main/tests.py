from django.test import TestCase
from django.urls import reverse

from main.models import Category


class HomePageTest(TestCase):
    def test_view_url_existing_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_by_url_name(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/store.html')
        self.assertTemplateNotUsed(resp, 'main/cart.html')


class CategoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Smartphone', slug='smartphone')

    def test_string_representation(self):
        category = Category(name='Smartphone')
        self.assertEqual(str(category.name), self.category.name)

    def test_category_content(self):
        self.assertEqual(f'{self.category.name}', 'Smartphone')
        self.assertEqual(f'{self.category.slug}', 'smartphone')
