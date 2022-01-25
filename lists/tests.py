from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


# Create your tests here.
class HomePageTest(TestCase):

    # def test_home_page(self):
    #    found = resolve('/')
    #    self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

        '''
        # old code chapter 3
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        print((html  == expected_html))
        print(repr(html))'''

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def block_test_displays_all_list_items(self):
        Item.objects.create(text='itemey1')
        Item.objects.create(text='itemey2')

        response = self.client.get('/')

        self.assertIn('itemey1', response.content.decode())
        self.assertIn('itemey2', response.content.decode())


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_1 = List()
        list_1.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_1
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_1
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_1)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(first_saved_item.list, saved_list)
        self.assertEqual(second_saved_item.list, saved_list)


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


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_can_redirect(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, f'/lists/{List.objects.first().id}/')

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item ot existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item ot existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item ot existing list'})
        self.assertRedirects(response,f'/lists/{correct_list.id}/')