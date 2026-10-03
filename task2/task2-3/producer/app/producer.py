import os
import time
import pika

def main():
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
    
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

    counter = 1
    print(" [*] Producer started generating tasks...")
    
    try:
        while True:
            message = f"Task #{counter} generated at {time.strftime('%Y-%m-%d %H:%M:%S')}"
            channel.basic_publish(
                exchange='',
                routing_key='task_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                )
            )
            print(f" [x] Sent: '{message}'")
            counter += 1
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping Producer...")
        connection.close()

if __name__ == '__main__':
    main()