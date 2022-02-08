from django.test import TestCase
from lists.models import Item, List
from django.utils.html import escape



# Create your tests here.
# noinspection PyUnresolvedReferences
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_1 = List.objects.create()
        response = self.client.get(f'/lists/{list_1.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        w_list = List.objects.create()
        list_1 = List.objects.create()
        response = self.client.get(f'/lists/{list_1.id}/')
        self.assertEqual(response.context['list'], list_1)

    def test_displays_only_items_for_that_list(self):
        list_1 = List.objects.create()
        Item.objects.create(text='itemey1', list=list_1)
        Item.objects.create(text='itemey2', list=list_1)

        list_2 = List.objects.create()
        Item.objects.create(text='itemey3', list=list_2)
        Item.objects.create(text='itemey4', list=list_2)

        response = self.client.get(f'/lists/{list_1.id}/')

        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')
        self.assertNotContains(response, 'itemey3')
        self.assertNotContains(response, 'itemey4')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': "A new item for an existing text"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing text")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': "A new item for an existing text"}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        list_1 = List.objects.create()
        response = self.client.post(
            f'/lists/{list_1.id}/',
            data={'item_text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, escape("You can't have an empty list item"))

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_can_redirect(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, f'/lists/{List.objects.first().id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text' : ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

