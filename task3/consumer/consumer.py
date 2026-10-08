import os
import time
import json
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
TOPIC = os.environ.get('KAFKA_TOPIC', 'test-topic')
GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'my-consumer-group')

consumer = None
while not consumer:
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=GROUP_ID,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Successfully connected to Kafka Consumer", flush=True)
    except Exception as e:
        print(f"Waiting for Kafka broker... Error: {e}", flush=True)
        time.sleep(5)

print("[Consumer] Waiting for messages...", flush=True)
for message in consumer:
    print(f"[Consumer] Received: {message.value} from partition {message.partition} at offset {message.offset}", flush=True)