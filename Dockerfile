FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ server/
COPY client/ client/

ENV PYTHONUNBUFFERED=1
ENV GRPC_PORT=50051
EXPOSE 50051

CMD ["python", "server/app.py"]
