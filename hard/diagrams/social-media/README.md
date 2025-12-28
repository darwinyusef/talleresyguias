# 📱 Diagramas para Redes Sociales

Versiones ultra-simplificadas de las arquitecturas más reconocidas, optimizadas para compartir en redes sociales.

## 📊 Características

- ✅ **Ultra minimalistas**: 3-4 elementos máximo
- ✅ **Visual-first**: Menos texto, más impacto
- ✅ **Formato cuadrado**: Ideal para Instagram/LinkedIn/Twitter
- ✅ **Mensaje clave** en 1 línea
- ✅ **Tamaño Canvas**: ~600x800px (formato vertical mobile-friendly)

## 🎨 Diagramas Disponibles

### Semana 1: Fundamentos

1. **01-hexagonal-social.canvas** 🏛️
   - Concepto: Core + Adapters
   - Mensaje: "Aisla tu lógica de negocio"
   - Beneficio destacado: Cambia DB sin tocar core

2. **02-clean-social.canvas** 🎯
   - Concepto: 4 Layers (Frameworks → Entities)
   - Mensaje: "Dependencias → ADENTRO"
   - Regla: Entities NO conocen nada

3. **03-cqrs-social.canvas** ⚡
   - Concepto: Write vs Read
   - Mensaje: "Separa Lectura & Escritura"
   - Beneficio: Escala reads ≠ writes

4. **04-event-sourcing-social.canvas** 📚
   - Concepto: Events = Estado
   - Mensaje: "Estado = Σ(eventos)"
   - Beneficio: Time travel + Auditoría

5. **05-microservices-social.canvas** 🚀
   - Concepto: Servicios independientes
   - Mensaje: "Pequeños, Independientes"
   - Advertencia: Complejidad distribuida

### Semana 2: Patrones Modernos

6. **06-serverless-social.canvas** ⚡
   - Concepto: Lambda + DynamoDB
   - Mensaje: "Zero Servers, Full Power"
   - Dato: 1M requests = $5/month

7. **07-event-driven-social.canvas** 🚌
   - Concepto: Producer → Bus → Consumers
   - Mensaje: "Desacoplamiento Total"
   - Beneficio: 1 Producer → N Consumers

8. **08-api-gateway-social.canvas** 🚪
   - Concepto: Single Entry Point
   - Mensaje: "Single Entry Point"
   - Funciones: Auth + Rate Limit + Routing

9. **09-bff-social.canvas** 🔷
   - Concepto: Backend dedicado por frontend
   - Mensaje: "Backend for Frontend"
   - Beneficio: Optimizado por cliente

10. **10-saga-social.canvas** ⚙️
    - Concepto: Orchestration vs Choreography
    - Mensaje: "Transacciones Distribuidas"
    - Clave: Compensaciones automáticas

## 🎯 Cómo Usar

### Para Instagram/LinkedIn
1. Abrir el archivo `.canvas` en Obsidian
2. Tomar screenshot (formato cuadrado 1080x1080)
3. Agregar tu marca/logo si deseas
4. Hashtags sugeridos:
   - #SoftwareArchitecture
   - #SystemDesign
   - #TechLeadership
   - #Microservices
   - #CloudArchitecture

### Para Twitter/X
1. Usar el mismo screenshot
2. Tweet corto + diagrama
3. Thread con detalles técnicos
4. Link al diagrama completo

### Para Carrusel
1. Combinar 3-4 diagramas relacionados
2. Ejemplo: Hexagonal → Clean → CQRS
3. Contar una historia de evolución

## 📝 Template de Post

```
🏛️ [NOMBRE ARQUITECTURA]

[MENSAJE CLAVE EN 1 LÍNEA]

✅ Beneficio 1
✅ Beneficio 2
⚠️ Consideración importante

¿Cuándo usarla?
[Contexto específico]

#SoftwareArchitecture #SystemDesign
```

## 🎨 Paleta de Colores

- 🔴 Rojo (1): Servicios/Componentes principales
- 🟠 Naranja (2): Advertencias/Trade-offs
- 🟡 Amarillo (3): Clientes/Usuarios
- 🟢 Verde (4): Infraestructura/Datos
- 🟣 Morado (5): Middleware/Gateways
- 🔵 Azul (6): Títulos/Metadata

## 📈 Engagement Tips

1. **Mejor hora para publicar**: Martes-Jueves 9-11am
2. **Frecuencia**: 2-3 diagramas por semana
3. **Formato**: Carrusel > Single image
4. **Caption**: Pregunta al final para engagement
5. **Call-to-action**: "¿Usas esta arquitectura? Comenta 👇"

## 🔄 Variaciones

Puedes crear variaciones de estos diagramas:
- **Versión oscura** (cambiar colores de fondo)
- **Con código** (agregar snippet de 3-4 líneas)
- **Con estadísticas** (ej: "Usado por Netflix, Uber, Spotify")
- **Con anti-patterns** (qué NO hacer)

## 📚 Serie Completa

Estos 10 diagramas forman una serie cohesiva que cubre:
- **Fundamentos** (1-5): Bases arquitectónicas
- **Patrones Modernos** (6-10): Cloud & Distributed Systems

Próximamente:
- **Semana 3**: Escalabilidad & Resiliencia
- **Semana 4**: AI & Data Architectures
