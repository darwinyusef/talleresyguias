@echo off
REM Script de ejemplo para el taller
REM Este script demuestra funcionalidades básicas de batch

echo ==========================================
echo Script de Ejemplo - Batch (.bat)
echo ==========================================
echo.

REM Variables
set NOMBRE=Usuario
set FECHA=%DATE% %TIME%

echo Hola %NOMBRE%
echo Fecha actual: %FECHA%
echo.

REM Argumentos
echo Procesando argumentos...
echo Primer argumento: %1
echo Segundo argumento: %2
echo.

REM Directorio actual
echo Directorio actual:
cd
echo.

REM Listar archivos
echo Archivos en el directorio actual:
dir
echo.

REM Verificar si existe un archivo
set ARCHIVO=datos.txt
if exist "%ARCHIVO%" (
    echo El archivo %ARCHIVO% existe
    echo Contenido:
    type "%ARCHIVO%"
) else (
    echo El archivo %ARCHIVO% NO existe
    echo Creando archivo de ejemplo...
    echo Este es un archivo de ejemplo creado por el script > "%ARCHIVO%"
    echo Archivo creado exitosamente
)
echo.

REM Bucle simple
echo Contando del 1 al 5:
for %%i in (1 2 3 4 5) do (
    echo   Numero: %%i
)
echo.

REM Variables de entorno
echo Variables de entorno personalizadas:
if defined MI_VARIABLE (
    echo MI_VARIABLE: %MI_VARIABLE%
) else (
    echo MI_VARIABLE: No definida
)
if defined API_KEY (
    echo API_KEY: %API_KEY%
) else (
    echo API_KEY: No definida
)
echo.

REM Información del sistema
echo Informacion del sistema:
echo Usuario: %USERNAME%
echo Computadora: %COMPUTERNAME%
echo Sistema operativo: %OS%
echo.

echo ==========================================
echo Script completado exitosamente
echo ==========================================

exit /b 0
