#ТЗ итогового проекта «DRUMPAD»

_Изначально drumpad – приложение, используемое как электронная барабанная установка._ В своем приложении я попытаюсь воссоздать его функционал, а также добавить свои собственные функции.

Основные функции приложения:
*Воспроизведение семплов (т.е. звуков)
*Выбор из нескольких персетов, а также возможность создания своих собственных из файлов с устройства и из интернета
*Зацикливание звука
*Возможность войти под определенным логином и использовать созданные пользователем персеты без предварительной загрузки

Используемые технологии:
*PyQT5 для основного функционала
*pyaudio для работы со звуком
*requests для загрузки файлов из интернета
*time для зацикливания звуков
*SQL для хранения пользователей
