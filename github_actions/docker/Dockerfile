# Ejemplo de Dockerfile Multi-stage para entornos de CI/CD

# Stage 1: Build & Dependencies
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Instalamos solo lo necesario para el build
RUN npm ci
COPY . .
# RUN npm run build (si aplica)

# Stage 2: Production (Imagen final ligera)
FROM node:20-alpine
WORKDIR /app
# Copiamos solo los artefactos necesarios
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/src ./src

# Configuraciones de seguridad
EXPOSE 3000
USER node
CMD ["npm", "start"]
