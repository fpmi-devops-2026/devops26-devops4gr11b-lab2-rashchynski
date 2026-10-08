import time
import json
import os
import random
from kafka import KafkaProducer

bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
topic_name = 'lab2-topic'

print(f"Connecting to Kafka Producer at {bootstrap_servers}...", flush=True)

producer = None
for i in range(30):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka Producer successfully!", flush=True)
        break
    except Exception as e:
        print(f"Waiting for Kafka broker... ({e})", flush=True)
        time.sleep(2)

if not producer:
    raise Exception("Could not connect to Kafka Broker")

# Генерируем количество сообщений в диапазоне от 10 до 15
num_messages = random.randint(10, 15)
print(f"[Producer] Preparing to send {num_messages} messages...", flush=True)

for i in range(1, num_messages + 1):
    payload = {
        'event_id': i,
        'message': f'Kafka log event #{i}'
    }
    producer.send(topic_name, payload)
    print(f"[Producer] Sent: {payload}", flush=True)
    time.sleep(0.1)  # Небольшая задержка между отправками

# Отправляем Poison Pill (сигнал остановки)
stop_signal = {'action': 'stop'}
producer.send(topic_name, stop_signal)
print("[Producer] Sent STOP signal", flush=True)

producer.flush()
producer.close()
print("All messages sent successfully!", flush=True)