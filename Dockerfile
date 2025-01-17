FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x scripts/start.sh

EXPOSE 8000

CMD ["./scripts/start.sh"]
