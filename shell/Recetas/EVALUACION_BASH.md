# Evaluación de Bash Básico y Gestión de Archivos

Esta evaluación está diseñada para poner a prueba tus conocimientos sobre comandos básicos de terminal, navegación, manipulación de archivos y uso de editores de texto (Vim/Nano).

**Requisitos previos:**
- Tener acceso a una terminal Bash.
- Estar ubicado en la carpeta `Recetas` para los ejercicios prácticos.

---

## Parte 1: Preguntas Teóricas (10 Puntos)

Responde a las siguientes preguntas seleccionando la opción correcta o completando el comando.

1. **¿Qué comando se utiliza para mostrar la ruta absoluta del directorio actual?**
   a) `ls`
   b) `cd`
   c) `pwd`
   d) `dir`

2. **Si deseas listar todos los archivos, incluidos los ocultos, con detalles de permisos y tamaño, ¿qué comando usarías?**
   a) `ls -lh`
   b) `ls -la`
   c) `ls -a`
   d) `ls -l`

3. **¿Cuál es el comando para crear una estructura de directorios anidados como `menu/semanal/lunes` en un solo paso?**
   a) `mkdir menu/semanal/lunes`
   b) `mkdir -r menu/semanal/lunes`
   c) `mkdir -p menu/semanal/lunes`
   d) `touch menu/semanal/lunes`

4. **Explica brevemente la diferencia entre `>` y `>>` al redirigir la salida de un comando.**
   *Respuesta:* _________________________________________________________________________

5. **¿Qué comando usarías para buscar todos los archivos con extensión `.txt` dentro del directorio actual y sus subdirectorios?**
   a) `grep -r ".txt" .`
   b) `find . -name "*.txt"`
   c) `locate *.txt`
   d) `search *.txt`

6. **Tienes un script llamado `cocinar.sh`. ¿Qué comando le otorga permisos de ejecución al propietario?**
   a) `chmod +x cocinar.sh`
   b) `chmod 444 cocinar.sh`
   c) `chown +x cocinar.sh`
   d) `chmod -x cocinar.sh`

7. **¿Qué tecla debes presionar en `vim` para pasar del "Modo Normal" al "Modo Insertar" y poder escribir texto?**
   a) `Esc`
   b) `:wq`
   c) `i`
   d) `v`

8. **¿Cómo guardarías y saldrías de un archivo en `nano`?**
   a) `Ctrl+O` luego `Enter`, y `Ctrl+X`
   b) `:wq`
   c) `Ctrl+C`
   d) `Esc` luego `save`

9. **¿Qué comando permite ver las últimas 10 líneas de un archivo llamado `log_cocina.txt`?**
   a) `head log_cocina.txt`
   b) `cat log_cocina.txt`
   c) `tail log_cocina.txt`
   d) `less log_cocina.txt`

10. **¿Cuál es el comando para renombrar un archivo `receta_vieja.txt` a `receta_nueva.txt`?**
    a) `cp receta_vieja.txt receta_nueva.txt`
    b) `mv receta_vieja.txt receta_nueva.txt`
    c) `rn receta_vieja.txt receta_nueva.txt`
    d) `touch receta_vieja.txt receta_nueva.txt`

---

## Parte 2: Ejercicios Prácticos (4 Prácticas)

Realiza las siguientes tareas en tu terminal dentro de la carpeta `Recetas`.

### Práctica 1: Organización y Exploración del Menú
**Objetivo:** Navegar y listar contenidos.

1. Abre tu terminal y navega hasta la carpeta `Recetas`.
2. Lista el contenido de la carpeta `Carnes` mostrando los detalles (permisos, usuario, tamaño).
3. Crea un archivo llamado `inventario_recetas.txt` en la raíz de `Recetas` que contenga el listado de todos los archivos `.txt` que existen dentro de las carpetas `Carnes`, `Ensaladas`, `Pastas` y `Postres`.
   > *Pista: Usa `find` o `ls` recursivo y redirecciona la salida.*

### Práctica 2: El Chef Digital (Creación de Archivos)
**Objetivo:** Usar `touch`, `vim` y `nano` para crear diferentes formatos.

1. Entra a la carpeta `Ensaladas`.
2. Usa **`vim`** para crear un archivo llamado `Ensalada_Cesar.md` (Markdown).
   - Dentro escribe:
     ```markdown
     # Ensalada César
     - Lechuga
     - Crutones
     - Queso Parmesano
     - Aderezo César
     ```
   - Guarda y sal (`:wq`).
3. Vuelve a la carpeta `Recetas` y entra en `Postres`.
4. Usa **`nano`** para crear un archivo llamado `precios_postres.csv` (CSV).
   - Dentro escribe:
     ```csv
     Postre,Precio
     Compota de Manzana,5.00
     Tarta de Frambuesa,8.50
     ```
   - Guarda y sal.
5. Usa **`touch`** para crear un archivo vacío llamado `notas_chef.json` en la carpeta `Pastas`.

### Práctica 3: Gestión de la Cocina (Manipulación de Archivos)
**Objetivo:** Copiar, mover y eliminar.

1. Crea una nueva carpeta en `Recetas` llamada `Favoritos`.
2. Copia el archivo `Entrecot al Malbec.txt` (que está en `Carnes`) dentro de la carpeta `Favoritos`.
3. Mueve el archivo `notas_chef.json` (que creaste en `Pastas`) a la raíz de `Recetas`.
4. Renombra `notas_chef.json` a `configuracion_cocina.json`.
5. Elimina (con precaución) el archivo original `Entrecot al Malbec.txt` de la carpeta `Carnes` (simulando que ahora solo existe en Favoritos). *Nota: Si prefieres no borrarlo, solo verifica que la copia en Favoritos exista.*

### Práctica 4: Auditoría y Búsqueda
**Objetivo:** Permisos, búsqueda y `grep`.

1. Asigna permisos de **solo lectura** para todos (usuario, grupo, otros) al archivo `configuracion_cocina.json` (chmod 444).
2. Verifica los permisos con `ls -l`.
3. Busca en todas las recetas (dentro de todas las carpetas) qué archivos contienen la palabra "Manzana" (o alguna palabra clave que sepas que existe en tus archivos actuales, como "Ricotta" o "Malbec").
   > *Comando sugerido: `grep -r "Manzana" .`*
4. (Opcional) Genera un archivo `resumen_busqueda.txt` con el resultado del comando anterior.

---
**¡Éxito en tu evaluación!**
