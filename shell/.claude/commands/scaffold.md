# Comando: /scaffold

Crea estructura inicial para nuevos componentes o módulos.

## Argumentos:
- `type`: Tipo de scaffold (component, api, model, service, etc.)
- `name`: Nombre del componente

## Ejemplos:
- `/scaffold component UserProfile`
- `/scaffold api posts`
- `/scaffold model User`

## Pasos:

1. Analiza el tipo de scaffold solicitado
2. Identifica la estructura y convenciones del proyecto
3. Genera archivos necesarios:
   - Código base con estructura correcta
   - Tests correspondientes
   - Archivos de configuración si aplica
4. Actualiza imports/exports necesarios
5. Muestra instrucciones de uso
