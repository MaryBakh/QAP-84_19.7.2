from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_fail_email(email=fail_email, password=valid_password):
    """ Запрос api ключа с пустым логином"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_api_key_for_fail_password(email=valid_email, password=fail_password):
    """ Запрос api ключа с некорректным паролем"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_successful_add_new_pet_simple(name='Махмуд', animal_type='Павук', age='2'):
    """Проверяем, что можно добавить питомца без фото с корректными данными"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_set_photo(name='Махмуд', animal_type='Павук', pet_photo='images/pawuk.jpeg'):
    """Проверяем, возможность обновления фото питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то пробуем обновить фото питомца
    pet_id = 0
    if len(my_pets['pets']) > 0:
        for pet in my_pets['pets']:
            if pet['name'] == name and pet['animal_type'] == animal_type:
                pet_id = pet['id']
                break
        status, result = pf.set_photo(auth_key, pet_id, pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_fail_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Передача некорректного {pet_id} при обновлений информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, fail_pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 400
        assert status == 400
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_fail_delete_self_pet():
    """Передача пустого {pet_id} при удалении питомца"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.delete_pet(auth_key, empty_pet_id)

    # Проверяем что статус ответа равен 404
    assert status == 404

def test_successful_add_new_pet_simple_dop(name='', animal_type='', age=''):
    """Проверяем, что можно добавить питомца с пустыми данными"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name

def test_fail_add_new_pet_incorrect_name(name='Fail#$^&*@', animal_type='Павук', age='2'):
    """Проверяем, что нельзя добавить питомца с некорректным именем"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_fail_add_new_pet_incorrect_type(name='Махмуд', animal_type='Fail#$^&*@', age='2'):
    """Проверяем, что нельзя добавить питомца с некорректным типом питомца"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name

def test_fail_add_new_pet_incorrect_age(name='Махмуд', animal_type='Павук', age='Сто'):
    """Проверяем, что нельзя добавить питомца с некорректным возрастом"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name