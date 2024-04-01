FROM python:3.11-slim

COPY . .
COPY ../database /bot/database
COPY ../monitoring /bot/monitoring
COPY ../requirements.txt .

RUN pip install -r requirements.txt
