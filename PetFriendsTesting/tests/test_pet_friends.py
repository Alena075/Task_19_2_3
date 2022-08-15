from api import PetFriends
from settings import valid_email, valid_password, no_valid_email, no_valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос API ключа возвращает статус 200 и в результате содержися слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_not_valid_user(email=no_valid_email, password=no_valid_password):
    """ Проверяем, что запрос API ключа с неверным email и паролем возвращает статус 403 и не содержися слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
    Далее используя этот ключ запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_kry = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_kry, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Пушистик', animal_type='котёнок', age='1', pet_photo= 'images/cat2.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    # Получаем полный путь к изображениею питомца и сохраняем в переменную pet_photo.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца.
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_add_new_pet_with_valid_data_no_photo(name='Пушистик', animal_type='котёнок', age='1'):
    """Проверяем, что можно добавить питомца с корректными данными без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца.
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result ['age'] == age


def test_add_new_pet_with_valid_data_no_photo_no_name(name='%#@*&', animal_type='крокозябрик', age='7'):
    """Проверяем, что можно добавить питомца с некорректным именем без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца.
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result ['age'] == age


def test_add_new_pet_with_valid_data_no_photo_negative_age(name='Филимон', animal_type='котяра', age='-7'):
    """Проверяем, что можно добавить питомца с некорректным именем без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца.
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result ['age'] == age


def test_add_new_pet_with_valid_data_no_photo_no_age(name='Шарик', animal_type='собаня', age=''):
    """Проверяем, что можно добавить питомца с пустым полем возраст без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца.
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result ['age'] == age


def test_add_new_pet_with_valid_data_no_photo_no_name_negative_age(name='', animal_type='нечто', age='777777'):
    """Проверяем, что можно добавить питомца с пустым полем имя и некорректным полем возраст без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца.
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result ['age'] == age


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если сптсок своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев.
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Тишка", "кот", "5", "images/c1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берем ID первого питомца из списка и отравляем на удаление.
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Запрашиваем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удаленного питомца.
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Джерри', animal_type='мышь', age=2):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, вид и возраст.
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному.
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев.
        raise Exception("Моих питомцев нет")


def test_rejection_update_self_pet_info_without_animal_type(name='Анфиска', animal_type='', age=3):
    """ Проверяем невозможность очистить типа питомца путём передачи пустого поля animal_type """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.my_pets)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    # Проверяем что статус ответа = 200 и тип питомца не пустой
    assert status == 200
    assert result['animal_type']
