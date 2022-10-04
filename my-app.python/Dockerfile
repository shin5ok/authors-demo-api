FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

USER nobody

CMD exec uvicorn main:app --host 0.0.0.0 --port 8080 --workers 8
