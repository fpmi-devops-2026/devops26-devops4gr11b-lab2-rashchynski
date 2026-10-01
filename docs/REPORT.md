# Отчет по Лабораторной работе №2

## Задание 1. Bind mounts и Docker Compose

### 1. Цель задания

Организовать взаимодействие двух зависимых контейнеров-воркеров с использованием монтирования связыванием (`bind mounts`) и оркестрации через `Docker Compose`.

---

### 2. Структура проекта

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
### 3. Описание работы сервисов
1) Worker 1 (worker1):
* Выбирает входной файл (например, test1.txt) из директории с данными.
* Копирует и подготавливает файл для передачи следующему сервису в примонтированную директорию /var/result/data.txt.
2) Worker 2 (worker2):
* Читает файл data.txt, сгенерированный сервисом worker1.
* Анализирует числа в файле, находит максимальное значение и количество элементов (например, Max number: 50, Count: 3).
* Сохраняет итоговый результат в файл /var/result/result.txt.

### 4. Проверка и запуск
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
nazar@MacBook-Air-Nazar task1 % docker compose down
```
```
[+] down 3/3
 ✔ Container worker2_container Removed                                                                              0.0s
 ✔ Container worker1_container Removed                                                                              0.0s
 ✔ Network task1_default       Removed                                                                              0.1s
```

---
