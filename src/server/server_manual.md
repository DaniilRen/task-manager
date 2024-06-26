# Инструкция по запуску сервера

## Подготовка

1. Установить Java
Установка Java 17 производится с [официального сайта](https://www.oracle.com/java/technologies/downloads/#jdk17-windows)

* Необходимо выбрать в списке в нижней части экрана версию JDK 17 и загрузить установщик `x64 MSI Installer`
* Запустить загрузчик и нажать кнопку `Install`
* Перезагрузить компьютер в случае появления соответствующего сообщения

Иногда после установки система не видит Java, в таком случае нужно вручную указать системные переменные. Чтобы это сделать:

* В строке "Поиск" выполните поиск: Система (Панель управления)
* Нажмите на ссылку Дополнительные параметры системы.
* Нажмите Переменные среды. В разделе Системные переменные нажмите кнопку Создать.
* В окне создания системной переменной укажите имя переменной `JAVA_HOME` и значени `C:\Program Files\Java\jdk-17\bin` в случае, если система уставлена на диске `C:\`. 
* Нажмите ОК. Закройте остальные открытые окна, нажимая ОК. 


2. Распаковать архив с программой в ту же папку

## Запуск сервера

1. Запустить терминал Powershell:
В строке поиска Windows вбиваем Powershell и открываем от имени администратора
2. Перейти в папку с программой сервера  
Пишем в терминале:

```bash
cd Downloads/task_manager/src/server/task_sheduler
```

3. Запустить сервер командой в терминале:

```bash
java -jar target/task_sheduler-1.0-SNAPSHOT.jar
```

Для работы сервера терминал должен оставаться запущенным, база данных сохраняется при следующих запусках