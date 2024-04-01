FROM python:3.11-slim

COPY . .
COPY ../database /monitoring/database
COPY ../requirements.txt .

RUN pip install -r requirements.txt
