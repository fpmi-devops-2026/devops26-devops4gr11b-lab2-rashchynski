import os
import time
import pika

def main():
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
    storage_path = '/app/storage/results.txt'

    os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host, connection_attempts=5, retry_delay=3)
            )
        except Exception as e:
            print(f"Waiting for RabbitMQ at {rabbitmq_host}... Error: {e}")
            time.sleep(3)

    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    print(' [*] Consumer waiting for messages...')

    def callback(ch, method, properties, body):
        message_text = body.decode()
        print(f" [x] Received: '{message_text}'")
        
        # Запись в файл на локальном монтируемом диске (bind mount)
        with open(storage_path, 'a', encoding='utf-8') as f:
            f.write(f"{message_text}\n")
            
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Consumer...")
        connection.close()

if __name__ == '__main__':
    main()