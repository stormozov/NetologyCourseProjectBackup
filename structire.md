# Структура проекта

## Корневой каталог

- **[backup.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/backup.py)**: Точка входа в программу, отвечающая за выполнение процесса резервного копирования
  фотографий.

- **[requirements.txt](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/requirements.txt)**: Список зависимостей, необходимых проекту.

## Модули
### —| VK Модули

- **[vk_api.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/vk_modules/vk_api.py)**: Модуль Python, включающий класс и функцию для взаимодействия с API VK.

- **[vk_photo_processor.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/vk_modules/vk_photo_processor.py)**: Модуль Python, включающий класс VKPhotoProcessor, который обрабатывает
  полученную по VK API информацию по фотографиям.

- **[utils.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/vk_modules/utils.py)**: Модуль Python, включающий служебные функции для работы с данными 
  фотографий.

### —| Модули Яндекс.Диска

- **[folder_utils.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/ya_disk_upload/folder_utils.py)**: Модуль, включающий класс Folder Utils, предназначен для создания папок на Яндекс.Диске.

- **[upload_utils.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/ya_disk_upload/upload_utils.py)**: Модуль, включающий класс Uploader, предназначен для загрузки фото на 
  Яндекс.Диск

- **[ya_disk_uploader.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/ya_disk_upload/ya_disk_uploader.py)**: Модуль, включающий класс YaDiskUploader, предназначен для объединения 
  вызова "_folder_utils.py_" и "_upload_utils.py_" модулей из одного модуля.

### —| Вспомогательные модули

- **[create_json.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/create_json/create_json.py)**: Модуль, отвечающий за создание JSON файла с информацией о загруженных фото 
  на диск.

- **[unix_to_date.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/unix_to_date/unix_to_date.py)**:Модуль Python, содержащий класс UnixToDate для преобразования временных меток
  Unix в читабельные даты.

- **[fetch_photos_info.py](https://github.com/stormozov/NetologyCourseProjectBackup/blob/main/modules/fetch_photos_info/fetch_photos_info.py)**: Модуль, отвечающий за получение фотографий по VK API

