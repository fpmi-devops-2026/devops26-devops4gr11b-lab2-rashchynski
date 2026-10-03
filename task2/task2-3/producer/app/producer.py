import time, json, os, pika

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')

def run():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    for i in range(1, 11):
        data = {"task_id": i, "payload": f"Sample message data #{i}"}
        message = json.dumps(data)
        
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        print(f" [Producer] Sent task #{i}")
        time.sleep(2)

    connection.close()

if __name__ == '__main__':
    time.sleep(5)
    run()