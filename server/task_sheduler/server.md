# Инструкция по запуску сервера

Серверная часть реализована на Java (17+) и Spring Boot.
Обмен данными между клиентом и сервером - Json по RestAPI.
Команды в инструкции написаны для 

## Подготовка к запуску

1. Установить Java 17

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-17-jdk openjdk-17-jre
java -version
```

2. Распаковать архив с программой

```bash
unzip remote_todo_code.zip -d <место_хранения_проекта>
```

## Запуск сервера

1. Запустить терминал
Нажимаем сочетание `ctrl` + `alt` + `t`
2. Перейти в папку с программой сервера
Пишем в терминале:

```bash
cd ~/<место_хранения_проекта>/remote_todo_code/server/task_sheduler
```

3. Запустить сервер командой:

```bash
java -jar target/task_sheduler-1.0-SNAPSHOT.jar
```

Терминал должен оставаться запущенным, база данных сохраняется при следующих запусках