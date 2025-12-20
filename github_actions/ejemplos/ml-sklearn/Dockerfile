FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecutar el entrenamiento al construir la imagen
RUN python src/train.py

CMD ["python", "src/train.py"]
