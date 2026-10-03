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
    channel.queue_declare(queue='ai_agent_queue', durable=True)

    print(' [*] AI Agent ready to process messages...')

    def callback(ch, method, properties, body):
        prompt = body.decode()
        print(f" [AI Agent] Processing prompt: '{prompt}'")
        # Здесь логика ИИ-агента
        response = f"AI Response to: {prompt}"
        print(f" [AI Agent] Result: '{response}'")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='ai_agent_queue', on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping AI Agent...")
        connection.close()

if __name__ == '__main__':
    main()