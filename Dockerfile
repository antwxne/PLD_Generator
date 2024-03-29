FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --upgrade --no-cache-dir

CMD python3 -m sources.main