FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV ELASTICSEARCH_HOST=http://elasticsearch:9200
ENV ELASTICSEARCH_PORT=9200


CMD ["uvicorn", "my_fastapi:app", "--host", "0.0.0.0", "--port", "5000"]
