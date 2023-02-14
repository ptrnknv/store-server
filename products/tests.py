from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from store.wsgi import *

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list_view(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(tuple(response.context_data['products']), tuple(self.products[:2]))

    def test_list_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            tuple(response.context_data['products']),
            tuple(self.products.filter(category_id=category.id))[:2]
        )

    def test_page_list_product(self):
        path = reverse('products:paginator')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            tuple(response.context_data['products']),
            tuple(self.products)[:2]
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
