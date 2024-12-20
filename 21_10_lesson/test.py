import requests
import unittest

class TestAPI(unittest.TestCase):

    base_url = 'http://localhost:5000/items'

    def test_api_flow(self):
        # 1. Проверяем начальное количество
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        initial_items = response.json()
        initial_count = len(initial_items)
        print('Initial GET:', initial_items)

        # 2. Добавляем
        new_item = {"name": "example"}
        response = requests.post(self.base_url, json=new_item)
        self.assertEqual(response.status_code, 201)  
        created_item = response.json() # Преобразуем тело ответа в формат JSON (созданный элемент)
        print('POST response:', created_item) # Печатаем ответ на POST-запрос (новый элемент)
        self.assertEqual(created_item['name'], new_item['name'])  # Проверим, что имя совпадает

        # 3. Проверяем количество 
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        updated_items = response.json()
        updated_count = len(updated_items)
        print('Updated GET:', updated_items)

        # 4. Увеличилось на 1
        self.assertEqual(updated_count, initial_count + 1)
        self.assertIn(created_item, updated_items)  # Элемент присутствует в обновленном списке

if __name__ == '__main__':
    unittest.main()
