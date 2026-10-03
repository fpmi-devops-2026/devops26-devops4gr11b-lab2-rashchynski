# Task 2.1 — RabbitMQ Snippets & CLI

В данном разделе собраны полезные CLI-команды для диагностики и управления RabbitMQ с помощью `rabbitmqctl` и `rabbitmq-plugins`. Сниппеты сохранены в формате JSON в файле `snippets.json`.

1. Зарегистрирована учетная запись на сервисе CloudAMQP и создан бесплатный инстанс (план Little Lemur).
2. Выполнена настройка сущностей в RabbitMQ Management Console:
   - **Exchange**: `test_exchange` (тип `direct`).
   - **Queue**: `test_queue`.
   - **Binding**: связали `test_exchange` и `test_queue` по ключу `test_key`.
3. Протестирована отправка сообщений через панель управления (Publish message) с `routing_key = test_key`.
4. Протестировано получение сообщений из очереди `test_queue` через раздел (Get messages).
5. Результаты конфигурации и пример опубликованного JSON-сообщения сохранены в `snippets.json`.
