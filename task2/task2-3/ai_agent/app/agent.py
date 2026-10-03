import time, os, pika

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')

def run():
    print(" [AI Agent] Initialized and monitoring system tasks...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='ai_tasks', durable=True)

    def callback(ch, method, properties, body):
        print(f" [AI Agent] Received request: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='ai_tasks', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    time.sleep(5)
    run()