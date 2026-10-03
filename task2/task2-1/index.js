const express = require('express');
const amqp = require('amqplib');

const app = express();
const port = process.env.PORT || 3000;
const amqpUrl = process.env.CLOUDAMQP_URL;

// Ручка для отправки сообщения через RabbitMQ
app.get('/send', async (req, res) => {
  try {
    const connection = await amqp.connect(amqpUrl);
    const channel = await connection.createChannel();
    
    const exchange = 'test_exchange';
    const routingKey = 'test_key';
    const msg = JSON.stringify({
      text: 'Message sent via Node.js Express code!',
      timestamp: new Date().toISOString()
    });

    await channel.assertExchange(exchange, 'direct', { durable: true });
    channel.publish(exchange, routingKey, Buffer.from(msg));

    console.log(" [x] Sent '%s'", msg);
    
    setTimeout(() => {
      connection.close();
    }, 500);

    res.json({ status: 'success', sent_message: JSON.parse(msg) });
  } catch (error) {
    console.error(error);
    res.status(500).json({ status: 'error', error: error.message });
  }
});

// Ручка для чтения одного сообщения из очереди
app.get('/read', async (req, res) => {
  try {
    const connection = await amqp.connect(amqpUrl);
    const channel = await connection.createChannel();
    
    const queue = 'test_queue';
    await channel.assertQueue(queue, { durable: true });

    // Получаем 1 сообщение из очереди
    const msg = await channel.get(queue, { noAck: false });

    if (msg) {
      const content = msg.content.toString();
      channel.ack(msg); // Подтверждаем обработку сообщения
      
      setTimeout(() => connection.close(), 500);
      return res.json({ status: 'success', received_message: JSON.parse(content) });
    } else {
      setTimeout(() => connection.close(), 500);
      return res.json({ status: 'empty', message: 'No messages in queue' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ status: 'error', error: error.message });
  }
});

app.get('/', (req, res) => {
  res.json({ message: 'Task 2-1 Express app with RabbitMQ integration' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});