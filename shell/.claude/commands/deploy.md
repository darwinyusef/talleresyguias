# Comando: /deploy

Despliega la aplicación al servidor especificado.

## Argumentos:
- `env` (opcional): production, staging, development (default: staging)

## Pasos:

1. Verifica que no haya cambios sin commit
2. Ejecuta los tests
3. Construye la aplicación
4. Despliega al entorno especificado
5. Verifica que el despliegue fue exitoso
6. Muestra la URL del sitio desplegado
