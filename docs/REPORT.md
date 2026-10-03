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
