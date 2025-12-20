# 🎯 Ejercicios: Kubernetes (Zero to Hero)

Desafíos prácticos para dominar la orquestación de contenedores.

---

## 🟢 Nivel 1: Conceptos Básicos (Pods y Deployments)

### Desafío 1.1: El Servidor Web
**Objetivo**: Desplegar un servidor Apache.
- Crea un `Deployment` con la imagen `httpd:2.4`.
- Escálalo manualmente a 5 replicas.
- Expónlo como un `Service` de tipo `NodePort`.

### Desafío 1.2: Inspección Profunda
**Objetivo**: Entender el estado de los recursos.
- Describe el Pod creado anteriormente.
- Encuentra la IP interna asignada al Pod.
- Cambia la imagen del Deployment a `httpd:latest` y observa el `RollingUpdate`.

---

## 🟡 Nivel 2: Configuración y Redes

### Desafío 2.1: Inyección de Configuración
**Objetivo**: Cambiar el comportamiento de una app sin reconstruir la imagen.
- Crea un `ConfigMap` con un mensaje personalizado.
- Crea un Pod que cargue ese ConfigMap como una variable de entorno.
- Verifica que la app lea el mensaje.

### Desafío 2.2: Secretos de Base de Datos
**Objetivo**: Manejo seguro de contraseñas.
- Crea un `Secret` con un password en base64.
- Monta ese secreto como un archivo dentro de un contenedor en `/etc/secrets/password`.

---

## 🔴 Nivel 3: Persistencia y Statefull Apps

### Desafío 3.1: Base de Datos con Memoria
**Objetivo**: Que los datos no se borren al reiniciar el Pod.
- Crea un `PersistentVolumeClaim` de 500Mi.
- Despliega una base de datos MySQL usando ese PVC.
- Borra el Pod de MySQL y verifica que los datos siguen ahí cuando se recrea el Pod.

---

## 🔥 Nivel 4: Alta Disponibilidad y Escalado

### Desafío 4.1: Autoscaling bajo presión
**Objetivo**: Que el clúster reaccione a la carga.
- Habilita el `metrics-server` en tu clúster.
- Crea un `HorizontalPodAutoscaler` (HPA).
- Genera stress de CPU artificialmente y observa cómo K8s crea nuevos Pods.

### Desafío 4.2: Health Checks Pro
**Objetivo**: Zero downtime por fallos de arranque.
- Crea un Deployment con una `ReadinessProbe` que falle los primeros 60 segundos.
- Observa cómo el `Service` no envía tráfico al Pod hasta que la sonda pasa a estado OK.

---

## 🏆 Desafío Final: El Gran Orquestador

**Escenario**: Desplegar una plataforma de E-commerce.
1.  **DB**: PostgreSQL en un namespace propio, con persistencia y secretos.
2.  **API**: 3 replicas, con liveness probes y configurada vía ConfigMap.
3.  **Frontend**: Servido por Nginx manejando el balanceo de carga.
4.  **Seguridad**: Todo el tráfico HTTP debe estar bloqueado excepto el del puerto 80 del Frontend.

---

## 🛠️ Nivel 5: Helm, seguridad y GitOps

### Desafío 5.1: Tu primer Helm Chart
**Objetivo**: Automatizar despliegues con plantillas.
- Crea un nuevo Chart llamado `my-website`.
- Define una variable en `values.yaml` para el número de réplicas.
- Instala el chart y verifica que las réplicas cambien al modificar el archivo.

### Desafío 5.2: Restricción de Tráfico (NetworkPolicies)
**Objetivo**: Seguridad "Zero Trust".
- Despliega dos pods: `frontend` y `backend`.
- Crea una `NetworkPolicy` que impida que cualquier pod hable con el `backend` excepto el `frontend`.
- Prueba la conexión usando `curl` desde ambos pods.

### Desafío 5.3: El ciclo GitOps (Teórico/Práctico)
**Objetivo**: Sincronización automática.
- Instala ArgoCD en tu clúster (`kubectl create namespace argocd`).
- Conecta un repositorio de Git con manifiestos YAML.
- Haz un push a Git y observa cómo ArgoCD despliega los cambios sin usar `kubectl`.

---

[Ir al Índice](./INDICE.md) • [Volver al README](./README.md)
