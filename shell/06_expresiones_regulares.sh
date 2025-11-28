#!/bin/bash

################################################################################
# SCRIPT 6: EXPRESIONES REGULARES Y PATTERN MATCHING
################################################################################
# Temas cubiertos:
# - Operador =~ para regex
# - Patrones con [[ ]]
# - grep con expresiones regulares
# - sed para búsqueda y reemplazo
# - awk para procesamiento de texto
# - Validaciones comunes (email, teléfono, URL, etc)
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 6: EXPRESIONES REGULARES Y PATTERN MATCHING"
echo "═══════════════════════════════════════════════════════════"
echo ""

TEMP_DIR="/tmp/bash_ejercicios"
mkdir -p "$TEMP_DIR"

# 1. PATTERN MATCHING BÁSICO CON [[ ]]
echo "--- 1. Pattern Matching Básico ---"
texto="archivo.txt"

if [[ $texto == *.txt ]]; then
    echo "✓ '$texto' termina en .txt"
fi

if [[ $texto == archivo.* ]]; then
    echo "✓ '$texto' empieza con 'archivo.'"
fi

if [[ $texto == *chivo* ]]; then
    echo "✓ '$texto' contiene 'chivo'"
fi
echo ""

# 2. EXPRESIONES REGULARES CON =~
echo "--- 2. Expresiones Regulares con =~ ---"
email="usuario@ejemplo.com"

if [[ $email =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "✓ '$email' es un email válido"
else
    echo "✗ '$email' no es un email válido"
fi

# Capturar grupos
if [[ $email =~ ^([^@]+)@([^@]+)$ ]]; then
    echo "  Usuario: ${BASH_REMATCH[1]}"
    echo "  Dominio: ${BASH_REMATCH[2]}"
fi
echo ""

# 3. VALIDACIÓN DE DIFERENTES FORMATOS
echo "--- 3. Validaciones Comunes ---"

# Validar teléfono
validar_telefono() {
    local tel=$1
    if [[ $tel =~ ^[0-9]{3}-[0-9]{3}-[0-9]{4}$ ]]; then
        echo "✓ Teléfono válido: $tel"
        return 0
    else
        echo "✗ Teléfono inválido: $tel (formato: 123-456-7890)"
        return 1
    fi
}

validar_telefono "555-123-4567"
validar_telefono "123456789"
echo ""

# Validar URL
validar_url() {
    local url=$1
    if [[ $url =~ ^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$ ]]; then
        echo "✓ URL válida: $url"
        return 0
    else
        echo "✗ URL inválida: $url"
        return 1
    fi
}

validar_url "https://www.ejemplo.com"
validar_url "http://ejemplo.com/path/to/page"
validar_url "www.ejemplo.com"
echo ""

# Validar dirección IP
validar_ip() {
    local ip=$1
    local octeto="([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    if [[ $ip =~ ^${octeto}\.${octeto}\.${octeto}\.${octeto}$ ]]; then
        echo "✓ IP válida: $ip"
        return 0
    else
        echo "✗ IP inválida: $ip"
        return 1
    fi
}

validar_ip "192.168.1.1"
validar_ip "256.1.1.1"
validar_ip "10.0.0.255"
echo ""

# 4. GREP CON EXPRESIONES REGULARES
echo "--- 4. Grep con Regex ---"
cat > "$TEMP_DIR/contactos.txt" << 'EOF'
Juan Pérez - juan@email.com - 555-1234
Ana García - ana.garcia@company.com - 555-5678
Pedro López - pedro123@mail.org - 555-9012
María Rodríguez - maria.r@domain.net - 555-3456
Carlos Martínez - carlos_m@test.com - 555-7890
EOF

echo "Archivo de contactos:"
cat "$TEMP_DIR/contactos.txt"
echo ""

echo "Emails que contienen números:"
grep -E '[a-z0-9]*[0-9]+[a-z0-9]*@' "$TEMP_DIR/contactos.txt"
echo ""

echo "Teléfonos que empiezan con 555-5 o 555-9:"
grep -E '555-[59][0-9]{3}' "$TEMP_DIR/contactos.txt"
echo ""

echo "Nombres que terminan en 'ez':"
grep -E '^[A-Z][a-z]+\s+[A-Z][a-z]*ez\b' "$TEMP_DIR/contactos.txt"
echo ""

# 5. SED PARA BÚSQUEDA Y REEMPLAZO
echo "--- 5. Sed - Búsqueda y Reemplazo ---"
cat > "$TEMP_DIR/codigo.txt" << 'EOF'
var nombre = "Juan";
var edad = 25;
var ciudad = "Madrid";
EOF

echo "Código original:"
cat "$TEMP_DIR/codigo.txt"
echo ""

echo "Reemplazar 'var' con 'let':"
sed 's/var/let/g' "$TEMP_DIR/codigo.txt"
echo ""

echo "Extraer solo los valores entre comillas:"
sed -n 's/.*"\([^"]*\)".*/\1/p' "$TEMP_DIR/codigo.txt"
echo ""

echo "Añadir punto y coma al final si no lo tiene:"
sed 's/\([^;]\)$/\1;/' "$TEMP_DIR/codigo.txt"
echo ""

# 6. AWK PARA PROCESAMIENTO
echo "--- 6. Awk - Procesamiento de Texto ---"
cat > "$TEMP_DIR/ventas.txt" << 'EOF'
Producto Cantidad Precio
Laptop 5 1200
Mouse 15 25
Teclado 10 75
Monitor 8 300
EOF

echo "Tabla de ventas:"
cat "$TEMP_DIR/ventas.txt"
echo ""

echo "Calcular total por producto:"
awk 'NR>1 {total = $2 * $3; print $1 ": $" total}' "$TEMP_DIR/ventas.txt"
echo ""

echo "Total general de ventas:"
awk 'NR>1 {suma += $2 * $3} END {print "Total: $" suma}' "$TEMP_DIR/ventas.txt"
echo ""

echo "Productos con precio > 50:"
awk '$3 > 50 {print $1 " - $" $3}' "$TEMP_DIR/ventas.txt"
echo ""

# 7. EJERCICIO: Extractor de datos
echo "--- 7. Ejercicio: Extractor de Información ---"
cat > "$TEMP_DIR/log_server.txt" << 'EOF'
2024-01-15 10:23:45 [INFO] Server started on port 8080
2024-01-15 10:24:12 [ERROR] Connection failed to database
2024-01-15 10:24:13 [WARNING] Retrying connection...
2024-01-15 10:24:15 [INFO] Database connected successfully
2024-01-15 10:25:30 [ERROR] Invalid user credentials
2024-01-15 10:26:45 [INFO] User logged in: john_doe
EOF

echo "Log del servidor:"
cat "$TEMP_DIR/log_server.txt"
echo ""

echo "Extraer solo timestamps y mensajes de ERROR:"
grep "ERROR" "$TEMP_DIR/log_server.txt" | sed 's/\([0-9-: ]*\).*ERROR\] \(.*\)/[\1] \2/'
echo ""

echo "Contar eventos por tipo:"
echo "INFO: $(grep -c INFO "$TEMP_DIR/log_server.txt")"
echo "ERROR: $(grep -c ERROR "$TEMP_DIR/log_server.txt")"
echo "WARNING: $(grep -c WARNING "$TEMP_DIR/log_server.txt")"
echo ""

# 8. EJERCICIO: Validador de contraseñas
echo "--- 8. Ejercicio: Validador de Contraseñas ---"
validar_password() {
    local pass=$1
    local errores=()

    # Longitud mínima
    if [[ ! $pass =~ .{8,} ]]; then
        errores+=("mínimo 8 caracteres")
    fi

    # Al menos una mayúscula
    if [[ ! $pass =~ [A-Z] ]]; then
        errores+=("al menos una mayúscula")
    fi

    # Al menos una minúscula
    if [[ ! $pass =~ [a-z] ]]; then
        errores+=("al menos una minúscula")
    fi

    # Al menos un número
    if [[ ! $pass =~ [0-9] ]]; then
        errores+=("al menos un número")
    fi

    # Al menos un carácter especial
    if [[ ! $pass =~ [!@#\$%^&*] ]]; then
        errores+=("al menos un carácter especial (!@#\$%^&*)")
    fi

    if [ ${#errores[@]} -eq 0 ]; then
        echo "✓ Contraseña válida: $pass"
        return 0
    else
        echo "✗ Contraseña inválida: $pass"
        for error in "${errores[@]}"; do
            echo "    - Falta: $error"
        done
        return 1
    fi
}

validar_password "MiPass123!"
validar_password "debil"
validar_password "SinNumeros!"
echo ""

# 9. EJERCICIO: Parser de configuración
echo "--- 9. Ejercicio: Parser de Config INI ---"
cat > "$TEMP_DIR/config.ini" << 'EOF'
[database]
host=localhost
port=5432
username=admin
password=secret123

[server]
port=8080
debug=true
max_connections=100

[logging]
level=INFO
file=/var/log/app.log
EOF

echo "Archivo de configuración:"
cat "$TEMP_DIR/config.ini"
echo ""

echo "Extraer configuración de [database]:"
sed -n '/^\[database\]/,/^\[/{/^\[database\]/d;/^\[/d;p}' "$TEMP_DIR/config.ini"
echo ""

echo "Obtener valor de 'port' en sección [server]:"
sed -n '/^\[server\]/,/^\[/{s/^port=//p}' "$TEMP_DIR/config.ini"
echo ""

# 10. EJERCICIO: Limpieza de datos
echo "--- 10. Ejercicio: Limpieza de Datos ---"
cat > "$TEMP_DIR/datos_sucios.csv" << 'EOF'
nombre,  edad,  email
Juan Pérez,  25,  juan@email.com
  Ana García,30,ana@email.com
Pedro  López,  28,  pedro@email.com
EOF

echo "Datos originales (con espacios extra):"
cat "$TEMP_DIR/datos_sucios.csv"
echo ""

echo "Datos limpios (sin espacios extra):"
sed 's/[[:space:]]*,[[:space:]]*/,/g; s/^[[:space:]]*//; s/[[:space:]]*$//' "$TEMP_DIR/datos_sucios.csv"
echo ""

# 11. EJERCICIO: Extractor de URLs
echo "--- 11. Ejercicio: Extractor de URLs ---"
cat > "$TEMP_DIR/texto_urls.txt" << 'EOF'
Visita https://www.ejemplo.com para más información.
También puedes revisar http://blog.ejemplo.org/articulo
O contactarnos en https://contact.ejemplo.net/form
EOF

echo "Texto con URLs:"
cat "$TEMP_DIR/texto_urls.txt"
echo ""

echo "URLs extraídas:"
grep -oE 'https?://[a-zA-Z0-9./?=_-]+' "$TEMP_DIR/texto_urls.txt"
echo ""

# 12. EJERCICIO: Formateador de números de teléfono
echo "--- 12. Ejercicio: Formatear Teléfonos ---"
formatear_telefono() {
    local tel=$1
    # Eliminar todo excepto dígitos
    local solo_digitos=$(echo "$tel" | tr -cd '0-9')

    if [ ${#solo_digitos} -eq 10 ]; then
        echo "${solo_digitos:0:3}-${solo_digitos:3:3}-${solo_digitos:6:4}"
    else
        echo "Error: número debe tener 10 dígitos"
    fi
}

echo "Formateando diferentes formatos de teléfono:"
formatear_telefono "5551234567"
formatear_telefono "(555) 123-4567"
formatear_telefono "555.123.4567"
formatear_telefono "555 123 4567"
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - Usa [[ ]] con =~ para regex en bash"
echo "   - BASH_REMATCH contiene los grupos capturados"
echo "   - grep -E para regex extendidas"
echo "   - sed 's/patrón/reemplazo/g' para reemplazar"
echo "   - awk es poderoso para procesar columnas"
echo "   - Escapa caracteres especiales: \$ \. \* \+ \? \[ \]"
echo "   - ^ = inicio, $ = final, . = cualquier carácter"
echo "   - * = 0 o más, + = 1 o más, ? = 0 o 1"
