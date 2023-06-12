import os.path

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_email(email='qqqq@qqqq.qq', password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при вводе неправильного e-mail"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_api_key_for_invalid_email_2(email='qqqq.qqqq.qq', password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при вводе некорректно заполненного e-mail"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_api_key_for_invalid_psw(email=valid_email, password='dsdfg'):
    """ Проверяем что запрос api ключа возвращает статус 403 при вводе неправильного пароля"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pet(name='Sobaka', animal_type='dog', age='4', pet_photo='images/111.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Проверяем, что статус 200 и имя последнего добавленного питомца совпадает с тем, которое мы добавили
    assert status == 200
    assert result['name'] == name

def test_post_new_pet_with_incorrect_age(name='Sobaka', animal_type='dog', age='-2', pet_photo='images/111.jpeg'):
    """Проверяем что можно добавить питомца с некорректным возрастом"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Проверяем, что статус отличается от статуса 200
    assert status != 200
    #Обнаружен баг - допускается добавление питомца с некорретным возрастом

def test_post_new_pet_with_incorrect_photo(name='Sobaka', animal_type='dog', age='4', pet_photo='images/duck.txt'):
    """Проверяем что нельзя добавить питомца с текстовым файлом вместо фото"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Проверяем, что статус 200 и имя последнего добавленного питомца совпадает с тем, которое мы добавили
    assert status != 200
    #Обнаружен баг - допускается добавить питомца с прикрепленным текстовым файлом, вместо фото

def test_delete_last_pet():
    """Проверяем возможность удаления последнего питомца"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем список своих питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(MyPets['pets']) == 0:
        pf.post_new_pet(auth_key, "Барсик", "кот", "1", "images/cat.jpeg")
        _, MyPets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id последнего добавленного питомца из списка и отправляем запрос на удаление
    pet_id = MyPets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    # Запрашиваем список своих питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    #Проверяем, что статус 200 и в списке питомцев нет питомца с id удаленного питомца
    assert status == 200
    assert pet_id not in MyPets.values()

def test_update_last_pet(name='Baton', animal_type='cat', age = 30):
    """Проверяем возможность обновления информации о питомце"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем список своих питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(MyPets['pets']) > 0:
        pet_id = MyPets['pets'][0]['id']
        status, result = pf.update_last_pet(auth_key, pet_id, name, animal_type, age)
        # Проверяем, что статус 200 и имя обновленного питомца совпадает с тем, которое мы обновили
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_update_last_pet_with_incorrect_age(name='Baton', animal_type='cat', age = -30):
    """Проверяем возможность обновления информации о питомце, с указанием некорректного возраста"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем список своих питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(MyPets['pets']) > 0:
        pet_id = MyPets['pets'][0]['id']
        status, result = pf.update_last_pet(auth_key, pet_id, name, animal_type, age)
        # Проверяем, что статус 200 и имя обновленного питомца совпадает с тем, которое мы обновили
        assert status != 200
        #Обнаружен баг - допускается изменить возраст на отрицательный
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_post_new_pet_without_photo(name='Птичка', animal_type='bird', age='1'):
    """Проверяем что можно добавить питомца с корректными данными без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем, что статус 200 и имя последнего добавленного питомца совпадает с тем, которое мы добавили
    assert status == 200
    assert result['name'] == name

def test_post_new_pet_without_photo_with_incorrect_age(name='Птичка', animal_type='bird', age='-1'):
    """Проверяем что нельзя добавить питомца с некорректным возрастом без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем, что статус 200 и имя последнего добавленного питомца совпадает с тем, которое мы добавили
    assert status != 200
    #Обнаружен баг - допускается добавление нового питомца с указанием отрицательного возраста

def test_update_photo_last_pet(pet_photo='images/duck.jpeg'):
    """Проверяем возможность обновления фото питомца"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем список своих питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #Добавляем нового питомца с фото, чтобы записать в переменную данные фото, для последюущего сравнения
    pf.post_new_pet(auth_key, name = 'Doggy', animal_type = 'dog', age = '2', pet_photo = 'images/duck.jpeg')
    #Запрашиваем обновленный список питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    #Записываем в переменную данные фото
    base64_1 = MyPets['pets'][0]['pet_photo']
    #Удаляем только что созданного питомца
    pf.delete_pet(auth_key, MyPets['pets'][0]['id'])
    #Обновляем список питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой, то пробуем обновить фото питомца
    if len(MyPets['pets']) > 0:
        pet_id = MyPets['pets'][0]['id']
        status, result = pf.update_photo_last_pet(auth_key, pet_id, pet_photo)

        # Проверяем, что статус 200 и обновленное фото совпадают
        assert status == 200
        # Загружаем актуальные данные питомцев, чтобы сравнить фото
        _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
        #Записываем в новую переменную данные загруженного фото
        base64_2 = MyPets['pets'][0]['pet_photo']
        #Сравниваем данные загруженных фото
        assert base64_1 == base64_2
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_update_photo_last_pet_as_txt_file(pet_photo='images/duck.txt'):
    """Проверяем возможность вместо фото питомца загрузить текстовый файл"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем список своих питомцев
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(MyPets['pets']) > 0:
        pet_id = MyPets['pets'][0]['id']
        status, result = pf.update_photo_last_pet(auth_key, pet_id, pet_photo)

        # Проверяем, что статус не 200
        assert status != 200
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")