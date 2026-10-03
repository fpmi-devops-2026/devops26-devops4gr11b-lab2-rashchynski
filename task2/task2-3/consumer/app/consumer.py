import time, json, os, pika

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
STORAGE_PATH = '/app/storage/results.txt'

def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    print(f" [Consumer] Processing task_id={data['task_id']}")
    
    os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)
    with open(STORAGE_PATH, 'a') as f:
        f.write(f"Processed task #{data['task_id']}: {data['payload']}\n")
    
    time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def run():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [Consumer] Waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    time.sleep(5)
    run()