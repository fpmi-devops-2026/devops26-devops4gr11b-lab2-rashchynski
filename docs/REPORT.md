# Отчет по Лабораторной работе №2

## Задание 1. Bind mounts и Docker Compose

### Цель задания

Организовать взаимодействие двух зависимых контейнеров-воркеров с использованием монтирования связыванием (`bind mounts`) и оркестрации через `Docker Compose`.

---

### Структура проекта

Код и конфигурации Задания 1 расположены в директории `task1/`:

```
task1/
├── compose.yaml
├── worker1/
│   ├── Dockerfile
│   └── app.py
├── worker2/
│   ├── Dockerfile
│   └── app.py
├── data/
├── result/
└── result-1/
```

### Описание работы сервисов

1. Worker 1 (worker1):

- Выбирает входной файл (например, test1.txt) из директории с данными.
- Копирует и подготавливает файл для передачи следующему сервису в примонтированную директорию /var/result/data.txt.

2. Worker 2 (worker2):

- Читает файл data.txt, сгенерированный сервисом worker1.
- Анализирует числа в файле, находит максимальное значение и количество элементов (например, Max number: 50, Count: 3).
- Сохраняет итоговый результат в файл /var/result/result.txt.

### Проверка и запуск

Запуск и сборка контейнеров выполняются из директории task1/:

```
docker compose up --build
```

```
[+] Building 5.7s (16/16) FINISHED
 => [internal] load local bake definitions                                                                         0.0s
 => => reading from stdin 1.14kB                                                                                   0.0s
 => [worker2 internal] load build definition from Dockerfile                                                       0.0s
 => => transferring dockerfile: 113B                                                                               0.0s
 => [worker1 internal] load build definition from Dockerfile                                                       0.0s
 => => transferring dockerfile: 113B                                                                               0.0s
 => [worker2 internal] load metadata for docker.io/library/python:3.11-slim                                        5.3s
 => [worker2 internal] load .dockerignore                                                                          0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [worker1 internal] load .dockerignore                                                                          0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [worker1 1/3] FROM docker.io/library/python:3.11-slim@sha256:e41613d42d4891e4930f79523f93f81bbc7632584ec65e36  0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:e41613d42d4891e4930f79523f93f81bbc7632584ec65e36ab055f41  0.0s
 => [worker2 internal] load build context                                                                          0.0s
 => => transferring context: 879B                                                                                  0.0s
 => [worker1 internal] load build context                                                                          0.0s
 => => transferring context: 778B                                                                                  0.0s
 => CACHED [worker1 2/3] WORKDIR /app                                                                              0.0s
 => CACHED [worker2 3/3] COPY app.py .                                                                             0.0s
 => CACHED [worker1 3/3] COPY app.py .                                                                             0.0s
 => [worker1] exporting to image                                                                                   0.0s
 => => exporting layers                                                                                            0.0s
 => => exporting manifest sha256:1242debd3fbd2081007135223b47b7c8bfad835bb86a52f4dab6df40d7f5aedf                  0.0s
 => => exporting config sha256:0cd0ede80076bf30f6ce2ba33b2c6118c005bab3b6f87dbd3df36f55b41cc4ec                    0.0s
 => => exporting attestation manifest sha256:9f99679006a1a96d458eeeb34205c7b5b4f251eec6b8c67b0680670358aeeecc      0.0s
 => => exporting manifest list sha256:c174a0dc4b6dd30268b0f0a10590b023b6c408dc5c136ef5d0646da58ef6126b             0.0s
 => => naming to docker.io/library/task1-worker1:latest                                                            0.0s
 => => unpacking to docker.io/library/task1-worker1:latest                                                         0.0s
 => [worker2] exporting to image                                                                                   0.0s
 => => exporting layers                                                                                            0.0s
 => => exporting manifest sha256:9828facb591a2096cee6ef20ae1e0d8061121ec188f54251ac9f89ad4f9456df                  0.0s
 => => exporting config sha256:c15624a75a05f1fd7a0566366f44827c5ad88a1c0ba2e21cc4fbf0fa92f6c746                    0.0s
 => => exporting attestation manifest sha256:3c4bf053ca6aced816a47023ef77ff5215e198030dbda046813e0e5e1603bdfd      0.0s
 => => exporting manifest list sha256:525d874e8b74f5cfc9f782e477a9917db3dbd47297bc92e8f4eb3804700cb7f3             0.0s
 => => naming to docker.io/library/task1-worker2:latest                                                            0.0s
 => => unpacking to docker.io/library/task1-worker2:latest                                                         0.0s
 => [worker2] resolving provenance for metadata file                                                               0.0s
 => [worker1] resolving provenance for metadata file                                                               0.0s
[+] up 2/2
 ✔ Image task1-worker2 Built                                                                                        5.7s
 ✔ Image task1-worker1 Built                                                                                        5.7s
Attaching to worker1_container, worker2_container
Container worker1_container Waiting
worker1_container  | [Worker 1] Selected file 'test1.txt' and copied to '/var/result/data.txt'
worker1_container exited with code 0
Container worker1_container Exited
worker2_container  | [Worker 2] Max number: 50, Count: 3
worker2_container  | [Worker 2] Result successfully saved to /var/result/result.txt
worker2_container exited with code 0
```

Оба воркера успешно отрабатывают последовательную цепочку задач и завершаются с кодом выходить 0.

```
docker compose down
```

```
[+] down 3/3
 ✔ Container worker2_container Removed                                                                              0.0s
 ✔ Container worker1_container Removed                                                                              0.0s
 ✔ Network task1_default       Removed                                                                              0.1s
```

---

## Задание 2.1 — Изучение брокера сообщений CloudAMQP

### Цель работы

Освоение базовых принципов работы брокера сообщений RabbitMQ, настройка базовых сущностей (Exchange, Queue, Binding) через облачный сервис CloudAMQP и проверка взаимодействия с брокером с помощью Node.js (amqplib).

### Выполненные шаги

1. **Создание и настройка инстанса CloudAMQP**:
   - Зарегистрирован аккаунт на платформе CloudAMQP.
   - Развернут инстанс RabbitMQ (план _Little Lemur_) на облачной инфраструктуре.
   - Получена строка подключения `amqps://...` для авторизации по протоколу AMQP с шифрованием SSL.

2. **Конфигурация сущностей в RabbitMQ Management**:
   - **Exchange**: Создана точка обмена `test_exchange` с типом `direct`.
   - **Queue**: Создана очередь сообщений `test_queue`.
   - **Binding**: Настроена связь между `test_exchange` и `test_queue` с маршрутизацией по ключу `test_key`.

3. **Разработка Node.js сервиса в Docker**:
   - В директории `task2-1` развернута независимая инфраструктура в контейнере Docker.
   - В файле `index.js` с использованием библиотеки `amqplib` реализованы эндпоинты API:
     - `GET /send` — публикация сообщения формата JSON в `test_exchange` с ключом `test_key`.
     - `GET /read` — вычитывание одного сообщения из `test_queue` с подтверждением приема (`ack`).
   - Переменные окружения с реквизитами доступа вынесены в изолированный файл `.env` (добавленный в `.gitignore`).

Сборка и запуск контейнера:

```
docker compose up -d --build
```

```
[+] Building 2.5s (12/12) FINISHED
=> [internal] load local bake definitions                                                             0.0s
=> => reading from stdin 602B                                                                         0.0s
=> [internal] load build definition from Dockerfile                                                   0.0s
=> => transferring dockerfile: 161B                                                                   0.0s
=> [internal] load metadata for docker.io/library/node:20-alpine                                      2.3s
=> [internal] load .dockerignore                                                                      0.0s
=> => transferring context: 76B                                                                       0.0s
=> [1/5] FROM docker.io/library/node:20-alpine@sha256:fb4cd12c85ee03686f6af5362a0b0d56d50c58a04632e6  0.0s
=> => resolve docker.io/library/node:20-alpine@sha256:fb4cd12c85ee03686f6af5362a0b0d56d50c58a04632e6  0.0s
=> [internal] load build context                                                                      0.0s
=> => transferring context: 422B                                                                      0.0s
=> CACHED [2/5] WORKDIR /app                                                                          0.0s
=> CACHED [3/5] COPY package*.json ./                                                                 0.0s
=> CACHED [4/5] RUN npm install --omit=dev                                                            0.0s
=> [5/5] COPY . .                                                                                     0.0s
=> exporting to image                                                                                 0.0s
=> => exporting layers                                                                                0.0s
=> => exporting manifest sha256:3c2e033bf4be4702dbb82294671a6048305c837a632c543a16ae2995230e871b      0.0s
=> => exporting config sha256:15d27b9fea8ae7c249d036cd1d4aa9735593a52fd7ac576b540bcd8229a31da1        0.0s
=> => exporting attestation manifest sha256:330a8fc1b3070c5e8387be265cab403e760890da699048d4f4a9c146  0.0s
=> => exporting manifest list sha256:aec90dffec1bb49a8d61d991eb3ec0a0f42e113e4d05d0d13b5a272ba5af548  0.0s
=> => naming to docker.io/library/task2-1-app:latest                                                  0.0s
=> => unpacking to docker.io/library/task2-1-app:latest                                               0.0s
=> resolving provenance for metadata file                                                             0.0s
[+] up 2/2
✔ Image task2-1-app       Built                                                                        2.6s
✔ Container task2-1-app-1 Started                                                                      0.7s
```

Результаты тестирования API
Публикация сообщения в RabbitMQ (/send):

```
curl http://localhost:3000/send
```

```
{"status":"success","sent_message":{"text":"Message sent via Node.js Express code!","timestamp":"2026-10-03T07:40:08.335Z"}}%
```

Вычитание сообщения из очереди CloudAMQP (/read):

```
curl http://localhost:3000/read
```

```
{"status":"success","received_message":{"message":"Hello from CloudAMQP!","status":"ok"}}%
```

---

## Упражнение 2.2. Локальное развертывание RabbitMQ и паттерны обмена сообщениями

### Описание задачи

Запуск брокера RabbitMQ в Docker-контейнере (`rabbitmq:3-management`) и практическое исследование паттернов обмена сообщениями на Python (библиотека `pika`).

Проверка статуса локального брокера RabbitMQ

```
docker compose up -d
```

```
[+] up 2/2
 ✔ Network task2-2_default    Created                                                     0.0s
 ✔ Container rabbitmq_local Started                                                     0.1s

nazar@MacBook-Air-Nazar task2-2 % docker compose ps
NAME             IMAGE                   COMMAND                 SERVICE    CREATED         STATUS                   PORTS
rabbitmq_local   rabbitmq:3-management   "docker-entrypoint.s…"   rabbitmq   7 seconds ago   Up 6 seconds (healthy)   0.0.0.0:5672->5672/tcp, [::]:5672->5672/tcp, 0.0.0.0:15672->15672/tcp, [::]:15672->15672/tcp
```

### Tutorial 1: Hello World (Point-to-Point)

Терминал 1 (Получатель receive.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_1/receive.py
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received Hello World!
```

Терминал 2 (Отправитель send.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_1/send.py
 [x] Sent 'Hello World!'
```

### Tutorial 2: Work Queues (Распределение задач)

Терминал 1 (Отправитель new_task.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_2/new_task.py First task.
 [x] Sent First task.
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_2/new_task.py Second task..
 [x] Sent Second task..
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_2/new_task.py Third task...
 [x] Sent Third task...
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_2/new_task.py Fourth task....
 [x] Sent Fourth task....
```

Терминал 2 (Воркер 1 worker.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_2/worker.py
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received First task.
 [x] Done
 [x] Received Third task...
 [x] Done
```

Терминал 3 (Воркер 2 worker.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_2/worker.py
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received Second task..
 [x] Done
 [x] Received Fourth task....
 [x] Done
```

Вывод: Задачи 1 и 3 ушли первому воркеру, а задачи 2 и 4 — второму. Нагрузка распределилась равномерно.

### Tutorial 3: Publish/Subscribe (Веерная рассылка)

Терминал 1 (Издатель emit_log.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_3/emit_log.py "Broadcast test log"
 [x] Sent Broadcast test log
```

Терминал 2 (Подписчик 1 receive_logs.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_3/receive_logs.py
 [*] Waiting for logs. To exit press CTRL+C
 [x] Broadcast test log
```

Терминал 3 (Подписчик 2 receive_logs.py):

```
nazar@MacBook-Air-Nazar task2-2 % python3 tutorial_3/receive_logs.py
 [*] Waiting for logs. To exit press CTRL+C
 [x] Broadcast test log
```

Вывод: Сообщение Broadcast test log было одновременно доставлено обоим активным подписчикам.

---

## Упражнение 2.3 Контейнеризованная распределенная система

### Описание задачи

Создание многоконтейнерного комплекса (RabbitMQ + Producer + Consumer + AI Agent) с использованием compose.yaml, точек монтирования (bind mounts) для локального хранения результатов и интеграцией диагностических утилит rabbitmqctl / rabbitmqadmin.

Запуск и статус контейнеров:

```
docker compose up --build -d
```

```
[+] Building 3.3s (28/28) FINISHED
 => [internal] load local bake definitions                                                             0.0s
 => => reading from stdin 1.75kB                                                                       0.0s
 => [ai_agent internal] load build definition from Dockerfile                                          0.0s
 => => transferring dockerfile: 201B                                                                   0.0s
 => [consumer internal] load build definition from Dockerfile                                          0.0s
 => => transferring dockerfile: 204B                                                                   0.0s
 => [producer internal] load build definition from Dockerfile                                          0.0s
 => => transferring dockerfile: 204B                                                                   0.0s
 => [producer internal] load metadata for docker.io/library/python:3.11-slim                           2.9s
 => [producer internal] load .dockerignore                                                             0.0s
 => => transferring context: 2B                                                                        0.0s
 => [ai_agent internal] load .dockerignore                                                             0.0s
 => => transferring context: 2B                                                                        0.0s
 => [consumer internal] load .dockerignore                                                             0.0s
 => => transferring context: 2B                                                                        0.0s
 => [ai_agent 1/5] FROM docker.io/library/python:3.11-slim@sha256:bab1b7ef4b450c81002278d035eff85ebe3  0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:bab1b7ef4b450c81002278d035eff85ebe394ae94df9  0.0s
 => [ai_agent internal] load build context                                                             0.0s
 => => transferring context: 92B                                                                       0.0s
 => [producer internal] load build context                                                             0.0s
 => => transferring context: 95B                                                                       0.0s
 => [consumer internal] load build context                                                             0.0s
 => => transferring context: 95B                                                                       0.0s
 => CACHED [consumer 2/5] WORKDIR /app                                                                 0.0s
 => CACHED [ai_agent 3/5] COPY requirements.txt .                                                      0.0s
 => CACHED [ai_agent 4/5] RUN pip install --no-cache-dir -r requirements.txt                           0.0s
 => CACHED [ai_agent 5/5] COPY app/ /app/                                                              0.0s
 => CACHED [producer 3/5] COPY requirements.txt .                                                      0.0s
 => CACHED [producer 4/5] RUN pip install --no-cache-dir -r requirements.txt                           0.0s
 => CACHED [producer 5/5] COPY app/ /app/                                                              0.0s
 => CACHED [consumer 3/5] COPY requirements.txt .                                                      0.0s
 => CACHED [consumer 4/5] RUN pip install --no-cache-dir -r requirements.txt                           0.0s
 => CACHED [consumer 5/5] COPY app/ /app/                                                              0.0s
 => [ai_agent] exporting to image                                                                      0.0s
 => => exporting layers                                                                                0.0s
 => => exporting manifest sha256:546907f8cb177f1a5c10e1c92c3968cce469437d6c3b39435b24eea4a6a548b2      0.0s
 => => exporting config sha256:bc8b760c9dd7424f86e4e21f01c9749e08986f59e06b6320bec1ff22295b87b4        0.0s
 => => exporting attestation manifest sha256:3eb15175f7215b86b59e45f5b1e2c93efd58b0046a945a686d9a7b27  0.0s
 => => exporting manifest list sha256:031a4bdea27a7a5d17525b880986dae8f6d3e38ce4207a54e2ae19060ba9b29  0.0s
 => => naming to docker.io/library/task2-3-ai_agent:latest                                             0.0s
 => => unpacking to docker.io/library/task2-3-ai_agent:latest                                          0.0s
 => [producer] exporting to image                                                                      0.1s
 => => exporting layers                                                                                0.0s
 => => exporting manifest sha256:a1715436e655087b84523f0854c896422241fe8ab2ce3d064e6f47e5d0eabd52      0.0s
 => => exporting config sha256:c7303dabb42f266158b5271a8d46f7a30aacc5e069d18c27eb1682eafb351896        0.0s
 => => exporting attestation manifest sha256:5609ef0abc6a488c51cb961f2d6414a3b2c7e78c6115e67def40a327  0.0s
 => => exporting manifest list sha256:b8eb3631d4c9cb6c6de90f77d167f7b7ffc7df67fd03d33009a8862645a12cf  0.0s
 => => naming to docker.io/library/task2-3-producer:latest                                             0.0s
 => => unpacking to docker.io/library/task2-3-producer:latest                                          0.0s
 => [consumer] exporting to image                                                                      0.1s
 => => exporting layers                                                                                0.0s
 => => exporting manifest sha256:df74f754f5215123473a9a77c1da3e28f92dd84832ae84b36cadbac132f8f8ad      0.0s
 => => exporting config sha256:b7ec9b29db33efefdbe609ddf0bd36431247759894372ef4ece2176724a8ccd6        0.0s
 => => exporting attestation manifest sha256:129f17d912462aa2ef3a66a7130f176565962d662ce178c133933fe2  0.0s
 => => exporting manifest list sha256:debb90f79f11bfb70d61b73b41a3f8b4a7767245a476ae773b48124dce62628  0.0s
 => => naming to docker.io/library/task2-3-consumer:latest                                             0.0s
 => => unpacking to docker.io/library/task2-3-consumer:latest                                          0.0s
 => [ai_agent] resolving provenance for metadata file                                                  0.0s
 => [producer] resolving provenance for metadata file                                                  0.0s
 => [consumer] resolving provenance for metadata file                                                  0.0s
[+] up 7/7
 ✔ Image task2-3-producer     Built                                                                     3.4s
 ✔ Image task2-3-consumer     Built                                                                     3.3s
 ✔ Image task2-3-ai_agent     Built                                                                     3.3s
 ✔ Container rabbitmq_task2_3 Healthy                                                                   9.6s
 ✔ Container consumer_task2_3 Started                                                                   0.1s
 ✔ Container ai_agent_task2_3 Started                                                                   0.1s
 ✔ Container producer_task2_3 Started
```

```
nazar@MacBook-Air-Nazar task2-3 % docker compose ps
NAME               IMAGE                   COMMAND                 SERVICE    CREATED         STATUS                  PORTS
ai_agent_task2_3   task2-3-ai_agent        "python -u agent.py"    ai_agent   3 minutes ago   Up 59 seconds
consumer_task2_3   task2-3-consumer        "python -u consumer.…"  consumer   3 minutes ago   Up 59 seconds
producer_task2_3   task2-3-producer        "python -u producer.…"  producer   3 minutes ago   Up 59 seconds
rabbitmq_task2_3   rabbitmq:3-management   "docker-entrypoint.s…"  rabbitmq   3 minutes ago   Up About a minute (healthy)   5672/tcp, 15672/tcp
```

Проверка хранения данных через Bind Mount

```
nazar@MacBook-Air-Nazar task2-3 % cat consumer/storage/results.txt
Processed task #1: Sample message data #1
Processed task #2: Sample message data #2
Processed task #3: Sample message data #3
Processed task #4: Sample message data #4
Processed task #5: Sample message data #5
Processed task #6: Sample message data #6
Processed task #7: Sample message data #7
Processed task #8: Sample message data #8
Processed task #9: Sample message data #9
Processed task #10: Sample message data #10
```

Диагностика через CLI утилиты RabbitMQ

```
nazar@MacBook-Air-Nazar task2-3 % docker exec -it rabbitmq_task2_3 rabbitmqctl list_queues
Listing queues for vhost / ...

nazar@MacBook-Air-Nazar task2-3 % docker exec -it rabbitmq_task2_3 rabbitmqadmin list queues
No items
```

---

## Задание 3. Развертывание Apache Kafka в Docker (KRaft) и создание обработчика логов

### Цель задания

Изучение архитектуры Apache Kafka, развертывание брокера в современном режиме **KRaft** (без зависимости от ZooKeeper), а также проектирование race-condition-free конвейера обработки сообщений (Producer–Consumer) с динамической генерацией событий и корректным завершением работы (Poison Pill).

### Структура проекта

Код и конфигурации Задания 3 расположены в директории `task3/`

### Описание архитектуры и компонентов

1. **Kafka Broker (`kafka_local`):**
   - Используется официальный образ `apache/kafka:latest`.
   - Запущен в режиме **KRaft** (`KAFKA_NODE_ID=1`, `KAFKA_PROCESS_ROLES=broker,controller`).
   - Настроены слушатели для внутренней коммуникации между контейнерами (`kafka:29092`) и для внешнего доступа с хост-системы (`localhost:9092`).

2. **AKHQ (`akhq_local`):**
   - Веб-интерфейс для визуального мониторинга топиков, партиций, офсетов и групп потребителей (доступен по адресу `http://localhost:8080`).

3. **Producer (`kafka_producer`):**
   - Написан на Python (`kafka-python-ng`).
   - Реализует устойчивый цикл подключения с обработкой исключения `NoBrokersAvailable`.
   - Генерирует случайное количество логических событий (от 10 до 15) в топик `lab2-topic`.
   - По окончании отправки пакета передает специальный управляющий объект **Poison Pill**: `{"action": "stop"}`.

4. **Consumer (`kafka_consumer`):**
   - Выполняет поиск топика `lab2-topic` и явно привязывается к партиции (`assign([TopicPartition('lab2-topic', 0)])`).
   - Принудительно сбрасывает указатель чтения на самый первый офсет (`seek_to_beginning()`), гарантируя вычитку всех ранее отправленных данных независимо от порядка старта сервисов.
   - Завершает свою работу со статусом `0` при обнаружении Poison Pill (`{"action": "stop"}`).

### Проверка и запуск

Запуск комплекса выполняется из директории `task3/`:

```
docker compose up --build
```

Логи сервиса Producer:

```
docker compose logs producer
```

```
kafka_producer  | Connecting to Kafka Producer at kafka:29092...
kafka_producer  | Waiting for Kafka broker... (NoBrokersAvailable)
kafka_producer  | Waiting for Kafka broker... (NoBrokersAvailable)
kafka_producer  | Connected to Kafka Producer successfully!
kafka_producer  | [Producer] Preparing to send 14 messages...
kafka_producer  | [Producer] Sent: {'event_id': 1, 'message': 'Kafka log event #1'}
kafka_producer  | [Producer] Sent: {'event_id': 2, 'message': 'Kafka log event #2'}
kafka_producer  | [Producer] Sent: {'event_id': 3, 'message': 'Kafka log event #3'}
...
kafka_producer  | [Producer] Sent: {'event_id': 14, 'message': 'Kafka log event #14'}
kafka_producer  | [Producer] Sent STOP signal
kafka_producer  | All messages sent successfully!
```

Логи сервиса Consumer:

```
docker compose logs consumer
```

```
kafka_consumer  | Connecting to Kafka Consumer at kafka:29092...
kafka_consumer  | Waiting for Kafka broker... (NoBrokersAvailable)
kafka_consumer  | Connected to Kafka Consumer successfully!
kafka_consumer  | Listening for messages starting from offset 0...
kafka_consumer  | [Consumer Received] [Offset 0]: Event #1 -> Kafka log event #1
kafka_consumer  | [Consumer Received] [Offset 1]: Event #2 -> Kafka log event #2
...
kafka_consumer  | [Consumer Received] [Offset 13]: Event #14 -> Kafka log event #14
kafka_consumer  | [Consumer]: Received 'stop' signal at offset 14! Shutting down...
kafka_consumer  | Consumer session completed successfully!
```

Контроль статуса контейнеров:

```
docker compose ps -a
```

```
NAME             IMAGE              COMMAND                  SERVICE          CREATED         STATUS                     PORTS
akhq_local       tchiotl/akhq       "/app/akhq"              akhq             5 minutes ago   Up 5 minutes               0.0.0.0:8080->8080/tcp
kafka_consumer   task3-consumer     "python -u consumer.py"  kafka_consumer   5 minutes ago   Exited (0) 4 minutes ago
kafka_local      apache/kafka:latest "/__cacert_entrypoin…"  kafka            5 minutes ago   Up 5 minutes (healthy)     0.0.0.0:9092->9092/tcp
kafka_producer   task3-producer     "python -u producer.py"  kafka_producer   5 minutes ago   Exited (0) 4 minutes ago
```

Оба воркера (kafka_producer и kafka_consumer) успешно выполнили свою задачу и завершили сессии с кодом выходить 0.

---

### Ответы на вопросы

Вот полный набор ответов на все 30 контрольных вопросов из методических указаний к Лабораторной работе №2, оформленный в формате **Markdown**.

---

# Ответы на контрольные вопросы к Лабораторной работе №2

### 1. Что такое обмен сообщениями (messaging) и какие проблемы в архитектуре ПО он решает?

**Обмен сообщениями (messaging)** — это способ асинхронного взаимодействия между компонентами распределенной системы путем передачи структурированных пакетов данных (сообщений) через промежуточный слой.

**Решаемые архитектурные проблемы:**

- **Жесткая связность (Tight Coupling):** Отправитель и получатель не знают о внутренней реализации друг друга.

- **Синхронные блокировки:** Серверу не нужно ждать завершения обработки запроса клиентом.
- **Ненадежность сети и сбои:** При падении получателя сообщения накапливаются в брокере и обрабатываются после восстановления.

- **Сглаживание пиковых нагрузок (Traffic Levelling / Rate Limiting):** Защищает медленные сервисы от падения при внезапных всплесках трафика.

---

### 2. Что такое брокер сообщений? Какова его роль в системе?

**Брокер сообщений (Message Broker)** — это специализированный программный модуль (посредник), отвечающий за прием, маршрутизацию, буферизацию, хранение и доставку сообщений от издателей (Producers) к потребителям (Consumers).

**Роль в системе:**

- Гарантия доставки и сохранения сообщений.

- Трансформация и маршрутизация данных.

- Декаплинг (развязка) сервисов по времени, месту и протоколам.

---

### 3. Перечислите и охарактеризуйте основные шаблоны (паттерны) обмена сообщениями.

- **Точка-Точка (Point-to-Point / Work Queues):** Сообщение отправляется в очередь и обрабатывается **строго одним** из доступных воркеров. Используется для распределения тяжелых задач.
- **Издатель-Подписчик (Publish/Subscribe / Fanout):** Сообщение рассылается **всем** активным подписчикам, подключенным к теме/обменнику.
- **Маршрутизация (Routing / Direct):** Сообщения доставляются только в те очереди, которые связаны с точкой обмена конкретным ключом маршрутизации (`Routing Key`).
- **Тематическая маршрутизация (Topics):** Сообщения фильтруются и доставляются на основе масок и шаблонов (например, `logs.error.*`).
- **Удаленный вызов процедур (RPC):** Запрос отправляется в очередь с указанием обратной очереди (`reply_to`) и идентификатора корреляции (`correlation_id`) для получения ответа.

---

### 4. Дайте определение RabbitMQ.

**RabbitMQ** — это популярный open-source брокер сообщений с высокой надежностью и гибкими возможностями маршрутизации, выступающий посредником между издателями и потребителями.

---

### 5. Какой протокол лежит в основе RabbitMQ?

В основе RabbitMQ лежит протокол **AMQP 0-9-1** (Advanced Message Queuing Protocol). Также поддерживаются протоколы AMQP 1.0, MQTT, STOMP и HTTP через плагины.

---

### 6. В RabbitMQ сообщения, принятые от приложения-продюсера (издателя), записываются …

… сначала в **точку обмена (Exchange)**, которая на основе правил связывания (Bindings) и ключа маршрутизации (Routing Key) перенаправляет их в соответствующие **очереди (Queues)**.

---

### 7. Объясните, что такое точка обмена (Exchange).

**Exchange (Точка обмена)** — это агент маршрутизации внутри RabbitMQ. Он принимает сообщения от продюсеров и определяет, в какую очередь (или очереди) их нужно направить, анализируя тип обменника, Routing Key и атрибуты сообщения.

---

### 8. Что такое Binding в RabbitMQ?

**Binding (Связь)** — это правило или "мост", связывающий конкретную очередь (Queue) с точкой обмена (Exchange). Связь может содержать ключ связывания (`Binding Key`), используемый для фильтрации сообщений.

---

### 9. Дайте определение Routing Key в RabbitMQ.

**Routing Key (Ключ маршрутизации)** — это строковый атрибут (метаданные), который продюсер прикрепляет к сообщению при публикации. Exchange использует этот ключ для принятия решения о том, в какие очереди отправить сообщение.

---

### 10. Опишите по шагам процесс маршрутизации сообщения в RabbitMQ (от продюсера до потребителя).

1. **Продюсер** подключается к брокеру, создает канал и публикует сообщение в Exchange, указывая `Routing Key`.
2. **Exchange** получает сообщение и проверяет свой тип (direct, fanout, topic, headers).
3. **Exchange** сравнивает `Routing Key` сообщения с `Binding Key` всех привязанных к нему очередей.
4. Сообщение дублируется и помещается во все **очереди**, чьи правила связывания совпали.
5. **RabbitMQ** доставляет сообщение подключенному **потребителю** (Push) или ждет, пока потребитель сам запросит его (Pull).

6. **Потребитель** обрабатывает сообщение и отправляет подтверждение (`ack`) брокеру.
7. **Брокер** удаляет подтвержденное сообщение из очереди.

---

### 11. Если необходимо просто распараллелить обработку сообщений, принятых от продюсера (издателя) по нескольким потребителям, какой тип обменника надо выбрать в RabbitMQ?

Для простого распараллеливания задач между воркерами (Work Queues) используется **Default Exchange (Анонимный/Прямой)** или тип **Direct Exchange**, где все воркеры читают из **одной общей очереди**.

---

### 12. Какие типы точек обмена (exchanges) существуют в RabbitMQ и в чем их принципиальные отличия?

- **Direct Exchange:** Доставляет сообщения в очереди на основе точного совпадения `Routing Key` и `Binding Key`.
- **Fanout Exchange:** Игнорирует `Routing Key` и веерно рассылает сообщение во **все** привязанные очереди (Publish/Subscribe).
- **Topic Exchange:** Маршрутизирует сообщения на основе сопоставления `Routing Key` с масками очередей (используются спецсимволы `*` — одно слово, `#` — ноль или более слов).
- **Headers Exchange:** Маршрутизирует сообщения на основе анализа заголовков (headers) в свойствах AMQP-сообщения, игнорируя `Routing Key`.

---

### 13. Обычно приложение-продюсер отправляя сообщение в RabbitMQ, отправляет его ……

… в **точку обмена (Exchange)**, указывая имя обменника и ключ маршрутизации (`Routing Key`), а не напрямую в очередь.

---

### 14. Как предотвратить потребление устаревших данных из RabbitMQ?

1. **TTL для сообщений (Expiration):** Задание времени жизни отдельного сообщения в миллисекундах.
2. **TTL для очереди (`x-message-ttl`):** Ограничение времени хранения всех сообщений в очереди.
3. **Использование Dead Letter Exchange (DLX):** Автоматический сброс/перенаправление просроченных сообщений в отдельный обменник.
4. **Auto-delete queues:** Автоматическое удаление очереди при отключении последнего потребителя.

---

### 15. По какому принципу LIFO или FIFO устроены очереди в RabbitMQ, в которые записываются сообщения?

Очереди в RabbitMQ устроены по принципу **FIFO (First In, First Out — первыми пришли, первыми ушли)**. Исключения составляют очереди с приоритетами (Priority Queues) и повторная отправка неподтвержденных сообщений (redelivery).

---

### 16. Для чего предназначен Server (Broker/Node) в RabbitMQ.

**Server (Node)** в RabbitMQ — это экземпляр приложения на платформе Erlang, который управляет сетевыми соединениями, хранит структуры данных (очереди, обменники), осуществляет маршрутизацию, обеспечивает аутентификацию, авторизацию и кластеризацию.

---

### 17. Опишите назначение Virtual Host (Vhost) в RabbitMQ.

**Virtual Host (Vhost)** обеспечивает виртуальное изолированное пространство внутри одного экземпляра RabbitMQ. Внутри каждого Vhost разделены свои очереди, обменники, пользователи и права доступа (аналог разделения баз данных в СУБД).

---

### 18. Что такое подтверждение сообщений (acknowledgments / ack, nack, reject) и зачем оно необходимо?

Это механизм надежности, информирующий брокер о статусе обработки сообщения потребителем:

- **`ack` (acknowledge):** Подтверждение успешной обработки. Брокер удаляет сообщение из очереди.
- **`nack` (negative acknowledge) / `reject`:** Сигнал об ошибке при обработке. Сообщение может быть либо повторно возвращено в очередь (`requeue=true`), либо сброшено/переправлено в DLX (`requeue=false`).

---

### 19. Чем отличаются долговечные (durable) и временные (transient) очереди и сообщения? Как это влияет на перезагрузку брокера?

- **Durable (Долговечные):** Метаданные очередей и/или сообщения сохраняются на диск. При перезагрузке брокера они полностью восстанавливаются.
- **Transient (Временные):** Хранятся только в оперативной памяти. При перезагрузке брокера или сбое сервиса они безвозвратно теряются.

---

### 20. Что такое Dead Letter Exchange (DLX) и какие сценарии его использования?

**Dead Letter Exchange (DLX)** — это обычный Exchange, в который RabbitMQ автоматически перенаправляет "отклоненные" сообщения из очереди.

**Сценарии использования:**

1. Обработка сообщений, завершившихся ошибкой (`basic.reject` / `basic.nack` с `requeue=false`).
2. Обработка сообщений с истекшим сроком жизни (TTL).
3. Обработка переполнения очереди (`x-max-length`).

---

### 21. Что такое Priority Queue в RabbitMQ и как она работает?

**Priority Queue** — это очередь, поддерживающая приоритетность сообщений (задается аргументом `x-max-priority`). Сообщения с более высоким числовым приоритетом перемещаются в начало очереди и доставляются потребителям раньше сообщений с низким приоритетом.

---

### 22. Дайте определение Apache Kafka. Какие основные задачи она решает и чем ее философия отличается от классического района/брокеров?

**Apache Kafka** — это распределенная платформа потоковой передачи событий (Event Streaming Platform), работающая как распределенный журнал фиксации (distributed commit log).

**Основные задачи:** Сбор, хранение и обработка гигантских объемов потоковых данных в реальном времени (метрики, логи, события).

**Отличие от классических брокеров (RabbitMQ):**

- **Pull вместо Push:** Консьюмеры сами запрашивают данные с нужной скоростью.
- **Хранение данных:** Сообщения не удаляются после чтения, а хранятся на диске заданное время (retention period).
- **Высокая производительность:** Распределенная архитектура позволяет обрабатывать миллионы событий в секунду за счет линейного чтения с диска.

---

### 23. Опишите архитектуру Kafka. Что такое Broker, Topic и Partition?

- **Broker:** Узел кластера Kafka, отвечающий за прием, хранение и отдачу сообщений.
- **Topic:** Логическая категория или имя потока данных, в который отправляются сообщения.
- **Partition:** Неделимая единица масштабирования и параллелизма. Топик нарезается на партиции, которые распределяются по брокерам. Сообщения внутри партиции имеют строгий порядок и уникальные номера (**Offsets**).

---

### 24. Что такое Consumer Group (группа потребителей) и как она влияет на масштабирование и распараллеливание чтения?

**Consumer Group** — это группа потребителей с общим `group.id`, работающих над обработкой сообщений одного топика.

- Каждый потребитель в группе вычитывает свою уникальную партицию (или несколько).
- Одна партиция **не может** обрабатываться более чем одним потребителем внутри одной группы.
- Это позволяет легко масштабировать чтение: добавив воркеров в группу (вплоть до числа партиций), можно параллельно обрабатывать поток данных без дублирования.

---

### 25. Что такое реплика (Replica)? Чем роль Leader отличается от роли Follower?

**Replica** — это копия партиции, хранящаяся на другом брокере для обеспечения отказоустойчивости.

- **Leader (Лидер):** Единственная реплика, принимающая все операции записи и чтения для данной партиции.
- **Follower (Ведомый):** Реплика, которая пассивно копирует данные с Лидера. При падении Лидера один из Followers автоматически выбирается новым Лидером.

---

### 26. Что такое ZooKeeper (или подсистема KRaft в новых версиях) и какова его роль в архитектуре Kafka?

Они выполняют роль оркестратора и хранилища метаданных кластера Kafka:

- **ZooKeeper (устаревший подход):** Внешняя распределенная система, которая отслеживает статус брокеров, выбирает контроллеры и хранит конфигурацию топиков.
- **KRaft (Kafka Raft Metadata Mode):** Современный встроенный механизм консенсуса (без ZooKeeper), где метаданные хранятся в специальном внутреннем топике Kafka, а функции управления берут на себя сами брокеры.

---

### 27. Что такое Kafka Streams и как он отличается от написания Consumer-приложений?

**Kafka Streams** — это высокоуровневая клиентская библиотека для построения приложений потоковой обработки и аналитики данных в реальном времени.

**Отличие от обычного Consumer:**

- Обычный Consumer просто вычитывает байты из очереди.
- Kafka Streams предоставляет декларативный DSL (фильтрация, объединение потоков `join`, агрегация, окконные функции `windowing`, ведение состояния `state stores`) без необходимости ручного управления офсетами и низкоуровневой логикой.

---

### 28. В чем заключаются фундаментальные архитектурные отличия между RabbitMQ и Apache Kafka (модель хранения, маршрутизация, состояние сообщений)?

| Критерий            | RabbitMQ                                              | Apache Kafka |
| ------------------- | ----------------------------------------------------- | ------------ |
| **Модель доставки** | **Push:** Брокер сам проталкивает данные подписчикам. |

| **Pull:** Потребители сами опрашивают брокер. |
| **Маршрутизация** | Гибкая и сложная (Exchanges, Routing Keys, Headers).

| Тупая/простая (только топики и партиции). |
| **Модель хранения** | Временная (сообщение удаляется сразу после подтверждения). | Постоянный журнал (сообщения хранятся N дней/гигабайт). |
| **Повторное чтение** | Невозможно после удаления из очереди. | Возможно путем сброса указателя (Offset). |
| **Производительность** | Высокая (тысячи сообщений/сек). | Экстремальная (миллионы сообщений/сек). |

---

### 29. Приведи примеры, в каких сценариях предпочтительнее использовать RabbitMQ, а в каких — Apache Kafka.

- **RabbitMQ предпочтительнее:**
- Фоновая обработка задач в веб-приложениях (например, генерация PDF, отправка email).
- Сложная гибкая маршрутизация сообщений по множеству правил.

- Необходимость приоритетных очередей и точечных подтверждений (RPC, финансовые операции).

- **Apache Kafka предпочтительнее:**
- Обработка логов, метрик и событий в реальном времени (Event Sourcing).
- Системы Big Data, аналитика и машинное обучение на потоковых данных.
- Сценарии, где требуется сохранять историю событий и возможность перечитывать данные за прошлые периоды.

---

### 30. Можно ли использовать RabbitMQ и Apache Kafka в одной архитектуре? Если да, то за какие зоны ответственности каждый из них будет отвечать?

**Да, их часто используют вместе в крупных enterprise-системах.**

**Разделение зон ответственности:**

- **Apache Kafka (Центральная шина событий / Магистраль):** Сбор и аккумулирование всех логов, метрик и сырых событий от сотен микросервисов, передача данных в DWH/Hadoop/ClickHouse.
- **RabbitMQ (Операционный брокер команд):** Управление точечными бизнес-транзакциями между конкретными сервисами, асинхронные задачи воркеров, где важна сложная маршрутизация и гарантии быстрого подтверждения.
