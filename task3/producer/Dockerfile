FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir kafka-python-ng

COPY producer.py .

CMD ["python", "-u", "producer.py"]