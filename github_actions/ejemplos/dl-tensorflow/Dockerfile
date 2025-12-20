FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias (TF es pesado)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p models
RUN python src/train_dl.py

CMD ["python", "src/train_dl.py"]
