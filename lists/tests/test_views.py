from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertRedirects(response, f'/lists/{List.objects.first().id}/')

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


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

    def test_displays_item_form(self):
        list_1 = List.objects.create()
        response = self.client.get(f'/lists/{list_1.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

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
            data={'text': "A new item for an existing text"}
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
            data={'text': "A new item for an existing text"}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


    def post_invalid_input(self):
        list_1 = List.objects.create()
        return self.client.post(
            f'/lists/{list_1.id}/',
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))


