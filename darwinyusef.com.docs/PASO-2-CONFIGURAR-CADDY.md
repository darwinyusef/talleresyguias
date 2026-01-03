# ™ PASO 2: Configurar Caddyfile y Desplegar

Guía paso a paso para configurar Caddy con tu email, actualizar variables de entorno y desplegar el portfolio con HTTPS automático.

---

## =Ë Índice

1. [Prerequisitos](#prerequisitos)
2. [Actualizar Caddyfile](#actualizar-caddyfile)
3. [Configurar Variables de Entorno](#configurar-variables-de-entorno)
4. [Preparar el Servidor](#preparar-el-servidor)
5. [Desplegar con Caddy](#desplegar-con-caddy)
6. [Verificación](#verificación)
7. [Monitoreo de Certificados](#monitoreo-de-certificados)

---

##  Prerequisitos

Antes de comenzar, asegúrate de haber completado:

- [x] **PASO 1:** DNS configurado y propagado
- [x] Todos los dominios resuelven a la IP del servidor
- [x] Acceso SSH al servidor
- [x] Docker y Docker Compose instalados

### Verificar DNS

```bash
# En tu computadora local, verifica que DNS esté propagado
dig darwinyusef.com +short

# Debe retornar la IP de tu servidor
# Si no, espera más tiempo para propagación
```

---

## =Ý Actualizar Caddyfile

### Paso 1: Conectar al Servidor

```bash
# Desde tu computadora local
ssh root@YOUR_SERVER_IP

# Navegar al proyecto
cd /opt/portfolio/astro-portfolio
```

### Paso 2: Editar Caddyfile

```bash
# Abrir Caddyfile con nano
nano Caddyfile
```

### Paso 3: Actualizar Email para Let's Encrypt

**Busca esta sección al inicio del archivo:**

```
{
	# Email para notificaciones de Let's Encrypt
	email your-email@example.com  #  CAMBIAR ESTO
```

**Cámbiala por tu email real:**

```
{
	# Email para notificaciones de Let's Encrypt
	email tu-email@gmail.com  #  Tu email real
```

**Ejemplo:**

```
{
	# Email para notificaciones de Let's Encrypt
	email darwin.yusef@gmail.com
```

**  IMPORTANTE:**
- Usa un email válido que revises
- Let's Encrypt enviará notificaciones de expiración aquí
- Solo recibirás emails si hay problemas con la renovación

### Paso 4: (Opcional) Configurar para Testing

Si quieres probar primero sin agotar el rate limit de Let's Encrypt:

**Descomenta esta línea:**

```
{
	email tu-email@gmail.com

	# Para testing, usa staging de Let's Encrypt
	acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
}
```

**Nota:** Los certificados de staging mostrarán advertencia en el navegador, pero puedes verificar que todo funciona. Después quita esta línea para obtener certificados reales.

### Paso 5: Verificar Dominios en Caddyfile

**Revisa que todos los dominios estén listados:**

```bash
# Buscar en el archivo (Ctrl+W en nano)
darwinyusef.com
www.darwinyusef.com
arquitectura.darwinyusef.com
blog.darwinyusef.com
api.darwinyusef.com
minio.darwinyusef.com
```

**Deberían estar así:**

```
darwinyusef.com, www.darwinyusef.com {
	reverse_proxy astro-portfolio:4321 {
		# ...
	}
}

arquitectura.darwinyusef.com {
	reverse_proxy astro-portfolio:4321 {
		# ...
	}
}

blog.darwinyusef.com {
	reverse_proxy astro-portfolio:4321 {
		# ...
	}
}

# ... etc
```

### Paso 6: Guardar Cambios

**En nano:**
- `Ctrl+O` (Write Out)
- `Enter` (confirmar nombre)
- `Ctrl+X` (salir)

### Paso 7: Validar Caddyfile

```bash
# Validar sintaxis del Caddyfile
docker run --rm -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile caddy:2.7-alpine caddy validate --config /etc/caddy/Caddyfile

# Debe decir:
# Valid configuration
```

**Si hay errores:**
- Revisar que no falten llaves `{` o `}`
- Verificar que los dominios estén bien escritos
- Asegurarte que el email esté entre comillas si tiene caracteres especiales

---

## = Configurar Variables de Entorno

### Paso 1: Crear archivo .env

```bash
# En /opt/portfolio/astro-portfolio
nano .env
```

### Paso 2: Agregar Configuración

**Copia y pega esto, actualizando con tus valores:**

```bash
# ============================================
# Configuración de Producción
# ============================================

# Entorno
NODE_ENV=production

# URL del sitio
SITE_URL=https://darwinyusef.com

# Puerto interno (no cambiar)
PORT=4321

# ============================================
# Minio Storage (Opcional)
# ============================================

# Credenciales de Minio
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=TuPasswordSuperSeguro123!

# URLs de Minio
MINIO_ENDPOINT=minio.darwinyusef.com
MINIO_PORT=443
MINIO_USE_SSL=true

# ============================================
# Email para Caddy (Let's Encrypt)
# ============================================

ACME_EMAIL=tu-email@gmail.com

# ============================================
# Configuración de Email SMTP (si aplica)
# ============================================

# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=tu-email@gmail.com
# SMTP_PASS=tu-app-password
```

### Paso 3: Personalizar Variables

**Actualiza estos valores:**

```bash
# 1. URL del sitio
SITE_URL=https://darwinyusef.com  #  Tu dominio

# 2. Credenciales de Minio (crea una contraseña segura)
MINIO_ROOT_USER=admin  #  Cambia si quieres
MINIO_ROOT_PASSWORD=CrearPasswordSeguro123!  #  IMPORTANTE: Cambia esto

# 3. Email para Let's Encrypt
ACME_EMAIL=tu-email@gmail.com  #  Tu email real
```

### Paso 4: Generar Password Seguro para Minio

```bash
# Generar password aleatorio
openssl rand -base64 32

# Ejemplo de salida:
# 8kF3mN9pQ2xR7yT6vL1sW4eH5jK0bC9a

# Copia este password y úsalo en MINIO_ROOT_PASSWORD
```

### Paso 5: Guardar .env

**En nano:**
- `Ctrl+O` (Write Out)
- `Enter`
- `Ctrl+X`

### Paso 6: Proteger .env

```bash
# Cambiar permisos para que solo root pueda leer
chmod 600 .env

# Verificar permisos
ls -la .env

# Debe mostrar: -rw------- (solo owner)
```

---

## =¥ Preparar el Servidor

### Paso 1: Verificar Estado Actual

```bash
# Ver contenedores corriendo
docker ps

# Si hay contenedores del portfolio corriendo, detenerlos
docker compose down
```

### Paso 2: Crear Directorio de Logs

```bash
# Crear carpeta para logs de Caddy
mkdir -p logs/caddy

# Verificar
ls -la logs/
```

### Paso 3: Verificar Archivos Necesarios

```bash
# En /opt/portfolio/astro-portfolio

# Verificar que existen los archivos
ls -la Caddyfile
ls -la docker-compose-caddy.yml
ls -la .env

# Deberías ver todos los archivos
```

### Paso 4: Verificar Puertos Disponibles

```bash
# Ver qué está usando los puertos 80 y 443
netstat -tulpn | grep -E ':(80|443) '

# Si hay algo (nginx, apache), detenerlo:
# systemctl stop nginx
# systemctl disable nginx

# O si es un contenedor:
# docker stop nombre-contenedor
```

### Paso 5: Configurar Firewall

```bash
# Verificar firewall
ufw status

# Si está activo, asegurar que estos puertos estén abiertos
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw allow 443/udp    # HTTP/3
ufw allow 22/tcp     # SSH

# Aplicar cambios
ufw reload

# Verificar
ufw status numbered
```

---

## =€ Desplegar con Caddy

### Paso 1: Pull Latest Changes (Si usas Git)

```bash
# Asegurarse de tener la última versión
cd /opt/portfolio
git pull origin main

# Navegar al directorio de la app
cd astro-portfolio
```

### Paso 2: Build y Deploy

```bash
# Levantar todos los servicios con Caddy
docker compose -f docker-compose-caddy.yml up -d --build

# Esto hará:
# 1. Build de la imagen del portfolio
# 2. Pull de Caddy y Minio
# 3. Crear red y volúmenes
# 4. Iniciar todos los contenedores
```

**Salida esperada:**

```
[+] Building 45.2s
[+] Running 6/6
  Network portfolio-network              Created
  Volume "portfolio-caddy-data"          Created
  Volume "portfolio-caddy-config"        Created
  Volume "portfolio-minio-data"          Created
  Container astro-portfolio              Started
  Container portfolio-caddy              Started
  Container portfolio-minio              Started
```

### Paso 3: Ver Logs en Tiempo Real

```bash
# Ver logs de todos los servicios
docker compose -f docker-compose-caddy.yml logs -f

# O logs específicos:
# Caddy
docker logs -f portfolio-caddy

# Portfolio
docker logs -f astro-portfolio

# Minio
docker logs -f portfolio-minio
```

### Paso 4: Monitorear Obtención de Certificados

**En los logs de Caddy verás:**

```
[INFO] Obtaining certificate for darwinyusef.com
[INFO] Obtaining certificate for www.darwinyusef.com
[INFO] Obtaining certificate for blog.darwinyusef.com
[INFO] Obtaining certificate for arquitectura.darwinyusef.com
[INFO] Obtaining certificate for api.darwinyusef.com
[INFO] Certificate obtained for darwinyusef.com
[INFO] Certificate obtained for www.darwinyusef.com
...
```

**Esto puede tomar 1-3 minutos.**

### Paso 5: Esperar a que Todo Inicie

```bash
# Esperar 1-2 minutos para que:
# - Portfolio inicie completamente
# - Caddy obtenga todos los certificados
# - Minio inicie (si está habilitado)

# Verificar estado de contenedores
docker ps

# Todos deben estar "Up" y saludables
```

---

##  Verificación

### Paso 1: Verificar Contenedores

```bash
# Ver todos los contenedores
docker ps

# Debe mostrar:
# CONTAINER ID   IMAGE                    STATUS
# xxxxxxxxxxxx   caddy:2.7-alpine        Up 2 minutes
# xxxxxxxxxxxx   astro-portfolio:latest  Up 2 minutes (healthy)
# xxxxxxxxxxxx   minio/minio:latest      Up 2 minutes (healthy)
```

### Paso 2: Test Local en el Servidor

```bash
# Test HTTP (debe redirigir a HTTPS)
curl -I http://localhost

# Test HTTPS local
curl -I -k https://localhost

# Test del portfolio
curl -I http://darwinyusef.com
```

### Paso 3: Test desde Navegador

**Abre en tu navegador:**

```
https://darwinyusef.com
https://www.darwinyusef.com
https://blog.darwinyusef.com
https://arquitectura.darwinyusef.com
https://api.darwinyusef.com
```

**Verifica:**
-  Carga el sitio correctamente
-  Candado verde (SSL válido)
-  Certificado de "Let's Encrypt"
-  HTTP redirige automáticamente a HTTPS

### Paso 4: Verificar Certificados SSL

**En el navegador:**

1. Click en el candado =
2. Click en "Certificado" o "Certificate"
3. Verificar:
   - **Issued by:** Let's Encrypt
   - **Issued to:** darwinyusef.com
   - **Valid until:** ~3 meses desde hoy

**Desde línea de comandos:**

```bash
# Ver detalles del certificado
echo | openssl s_client -connect darwinyusef.com:443 2>/dev/null | openssl x509 -noout -dates

# Debe mostrar:
# notBefore=Jan 3 12:34:56 2026 GMT
# notAfter=Apr 3 12:34:56 2026 GMT
```

### Paso 5: Test de Redirección HTTP ’ HTTPS

```bash
# Test que HTTP redirige a HTTPS
curl -I http://darwinyusef.com

# Debe mostrar:
# HTTP/1.1 308 Permanent Redirect
# Location: https://darwinyusef.com/
```

### Paso 6: Test de SSL Labs (Opcional)

Ve a: https://www.ssllabs.com/ssltest/

1. Ingresa: **darwinyusef.com**
2. Click **Submit**
3. Espera 2-3 minutos

**Resultado esperado:** Calificación A o A+

### Paso 7: Verificar Multilenguaje

```bash
# Test rutas en español
curl -I https://darwinyusef.com/

# Test rutas en inglés
curl -I https://darwinyusef.com/en/

# Test rutas en portugués
curl -I https://darwinyusef.com/pt/

# Todas deben retornar 200 OK
```

---

## = Monitoreo de Certificados

### Ver Certificados Activos

```bash
# Entrar al contenedor de Caddy
docker exec -it portfolio-caddy sh

# Listar certificados
caddy list-certificates

# Salir
exit
```

**Salida esperada:**

```
darwinyusef.com
  Subject: CN=darwinyusef.com
  Issuer: CN=Let's Encrypt
  Not Before: 2026-01-03 12:00:00 +0000 UTC
  Not After: 2026-04-03 12:00:00 +0000 UTC

www.darwinyusef.com
  Subject: CN=www.darwinyusef.com
  ...
```

### Ver Logs de Renovación

```bash
# Ver logs de Caddy
docker logs portfolio-caddy | grep -i "renew"

# O ver todos los logs relacionados con certificados
docker logs portfolio-caddy | grep -i "certificate"
```

### Renovación Automática

Caddy renovará automáticamente los certificados 30 días antes de expirar.

**No necesitas hacer nada, pero puedes verificar:**

```bash
# Ver logs en tiempo real
docker logs -f portfolio-caddy

# Buscar mensajes como:
# [INFO] Certificate for darwinyusef.com renewed successfully
```

---

## =Ê Comandos Útiles

### Ver Estado de Servicios

```bash
# Ver todos los servicios
docker compose -f docker-compose-caddy.yml ps

# Ver uso de recursos
docker stats

# Ver logs de Caddy
docker logs -f portfolio-caddy

# Ver logs de Portfolio
docker logs -f astro-portfolio
```

### Reiniciar Servicios

```bash
# Reiniciar Caddy (sin downtime)
docker exec portfolio-caddy caddy reload --config /etc/caddy/Caddyfile

# O reiniciar el contenedor
docker compose -f docker-compose-caddy.yml restart caddy

# Reiniciar Portfolio
docker compose -f docker-compose-caddy.yml restart portfolio

# Reiniciar todos
docker compose -f docker-compose-caddy.yml restart
```

### Detener Servicios

```bash
# Detener todos
docker compose -f docker-compose-caddy.yml down

# Detener y eliminar volúmenes (¡cuidado! elimina certificados)
docker compose -f docker-compose-caddy.yml down -v
```

### Actualizar Configuración

```bash
# Si cambias el Caddyfile
nano Caddyfile

# Validar
docker run --rm -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile caddy:2.7-alpine caddy validate --config /etc/caddy/Caddyfile

# Reload sin downtime
docker exec portfolio-caddy caddy reload --config /etc/caddy/Caddyfile
```

---

## = Troubleshooting

### Problema: "Failed to obtain certificate"

**Error en logs:**

```
[ERROR] Failed to obtain certificate for darwinyusef.com
```

**Posibles causas y soluciones:**

1. **DNS no propagado**
   ```bash
   # Verificar DNS
   dig darwinyusef.com +short

   # Si no resuelve, esperar más tiempo
   ```

2. **Puerto 80 o 443 bloqueado**
   ```bash
   # Verificar firewall
   ufw status | grep -E '80|443'

   # Abrir puertos
   ufw allow 80/tcp
   ufw allow 443/tcp
   ```

3. **Otro servicio usando puerto 80/443**
   ```bash
   # Ver qué está usando los puertos
   netstat -tulpn | grep -E ':(80|443) '

   # Detener el servicio conflictivo
   systemctl stop nginx
   ```

4. **Email inválido**
   ```bash
   # Verificar email en Caddyfile
   grep email Caddyfile

   # Debe ser un email válido
   ```

---

### Problema: "502 Bad Gateway"

**Solución:**

```bash
# 1. Verificar que portfolio está corriendo
docker ps | grep astro-portfolio

# 2. Ver logs de portfolio
docker logs astro-portfolio

# 3. Verificar health
docker inspect astro-portfolio | grep -A 10 Health

# 4. Reiniciar portfolio
docker compose -f docker-compose-caddy.yml restart portfolio
```

---

### Problema: Rate Limit de Let's Encrypt

**Error:**

```
too many certificates already issued for exact set of domains
```

**Solución:**

```bash
# 1. Usar staging para testing
nano Caddyfile

# Agregar:
{
	email tu-email@gmail.com
	acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
}

# 2. Reload
docker exec portfolio-caddy caddy reload --config /etc/caddy/Caddyfile

# 3. Cuando funcione, quitar staging y volver a cargar
```

**Rate limits de Let's Encrypt:**
- 50 certificados por dominio por semana
- 5 intentos fallidos por hora

---

### Problema: Redirect Loop

**Síntoma:** ERR_TOO_MANY_REDIRECTS

**Solución:**

```bash
# Verificar headers en Caddyfile
nano Caddyfile

# Debe tener:
reverse_proxy astro-portfolio:4321 {
    header_up X-Forwarded-Proto {scheme}
}

# Reload
docker exec portfolio-caddy caddy reload --config /etc/caddy/Caddyfile
```

---

##  Checklist Final

Antes de dar por completado:

- [ ] Caddyfile actualizado con email correcto
- [ ] .env creado con variables correctas
- [ ] Servicios levantados con docker compose
- [ ] Todos los contenedores están "Up"
- [ ] Portfolio accesible vía HTTPS
- [ ] Certificados SSL obtenidos
- [ ] Todos los dominios funcionan
- [ ] HTTP redirige a HTTPS
- [ ] No hay errores en logs
- [ ] Multilenguaje funciona (es, en, pt)

---

## <‰ Resultado Final

¡Felicidades! Tu portfolio ahora tiene:

-  **HTTPS automático** en todos los dominios
-  **Certificados válidos** de Let's Encrypt
-  **Renovación automática** de certificados
-  **HTTP/2 y HTTP/3** habilitados
-  **Compresión automática** (gzip/zstd)
-  **Headers de seguridad** configurados
-  **Soporte multilenguaje** (es/en/pt)
-  **Zero downtime** en actualizaciones

---

## =Þ Siguiente Paso

Ahora que tienes Caddy configurado:

=I **Opcional:** [Configurar GitHub Actions para Auto-Deploy](./GITHUB-ACTIONS-DEPLOY.md)

---

## =Ú Referencias

- [Caddy Documentation](https://caddyserver.com/docs/)
- [Let's Encrypt Rate Limits](https://letsencrypt.org/docs/rate-limits/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)

---

**¡Caddy configurado y funcionando! =€**

**Tiempo estimado:** 15-30 minutos + 2-5 minutos para certificados
