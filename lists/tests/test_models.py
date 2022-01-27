from django.test import TestCase
from lists.models import Item, List


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

