from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class GuideTestCase(TestCase):
    fixtures = ['guide.json']

    def setUp(self):
        self.client = APIClient()

    def test_get_list_guide(self):
        list_guide_url = reverse('list_guide')
        response = self.client.get(list_guide_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data[0].keys()), ['id', 'name', 'short_name', 'description', 'versions'])
        self.assertEqual(list(response.data[0].get('versions')[0].keys()), ['id', 'title', 'date_created'])

    def test_get_list_guide_selected_date(self):
        list_guide_url = reverse('list_guide')
        list_guide_url += '?date=2021-09-18'

        response = self.client.get(list_guide_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0].get('versions')), 2)

    def test_get_list_guide_selected_invalid_date(self):
        list_guide_url = reverse('list_guide')
        list_guide_url += '?date=18.09.2021'

        response = self.client.get(list_guide_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data[0].get('versions')), 2)

    def test_get_list_item_version_current(self):
        list_guide_item_url = reverse('list_guide_item_current',
                                      kwargs={'guide_pk': '34c40aeb-5866-4240-915d-c94526df3fbb'})
        response = self.client.get(list_guide_item_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data[0].keys()), ['code_item', 'value_item'])
        self.assertEqual(len(response.data), 2)

    def test_get_list_item_version_current_404(self):
        list_guide_item_url = reverse('list_guide_item_current',
                                      kwargs={'guide_pk': '34c40aeb-5866-4240-915d-c94526df3f22'})
        response = self.client.get(list_guide_item_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_item_selected_version(self):
        list_guide_item_url = reverse('list_guide_item_selected_version',
                                      kwargs={'version_pk': 'fc0d6d70-27e2-4b84-9074-ceb2904cbed7'})
        response = self.client.get(list_guide_item_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(list(response.data[0].keys()), ['code_item', 'value_item'])

    def test_get_list_item_selected_version_404(self):
        list_guide_item_url = reverse('list_guide_item_selected_version',
                                      kwargs={'version_pk': 'fc0d6d70-27e2-4b84-9074-ceb2904cbe22'})
        response = self.client.get(list_guide_item_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

