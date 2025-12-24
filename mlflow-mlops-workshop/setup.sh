#!/bin/bash

echo "========================================="
echo "MLflow MLOps Workshop - Setup Script"
echo "========================================="
echo ""

check_python() {
    echo "Verificando Python..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo "✓ Python $PYTHON_VERSION encontrado"
        return 0
    else
        echo "✗ Python 3 no encontrado. Por favor instala Python 3.8+"
        return 1
    fi
}

create_venv() {
    echo ""
    echo "Creando entorno virtual..."
    if [ -d "venv" ]; then
        echo "El entorno virtual ya existe. ¿Deseas recrearlo? (y/n)"
        read -r response
        if [[ "$response" == "y" ]]; then
            rm -rf venv
            python3 -m venv venv
            echo "✓ Entorno virtual recreado"
        else
            echo "Usando entorno virtual existente"
        fi
    else
        python3 -m venv venv
        echo "✓ Entorno virtual creado"
    fi
}

activate_venv() {
    echo ""
    echo "Activando entorno virtual..."
    source venv/bin/activate
    echo "✓ Entorno virtual activado"
}

install_dependencies() {
    echo ""
    echo "Instalando dependencias..."
    echo "Esto puede tomar 10-15 minutos..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet

    if [ $? -eq 0 ]; then
        echo "✓ Dependencias instaladas correctamente"
    else
        echo "✗ Error al instalar dependencias"
        return 1
    fi
}

create_directories() {
    echo ""
    echo "Creando directorios necesarios..."
    mkdir -p mlruns
    mkdir -p airflow/dags
    mkdir -p data
    mkdir -p logs
    echo "✓ Directorios creados"
}

setup_mlflow() {
    echo ""
    echo "Configurando MLflow..."

    cat > start_mlflow.sh << 'EOF'
#!/bin/bash
echo "Iniciando MLflow Tracking Server..."
source venv/bin/activate
mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
EOF

    chmod +x start_mlflow.sh
    echo "✓ Script de MLflow creado (./start_mlflow.sh)"
}

setup_airflow() {
    echo ""
    echo "¿Deseas configurar Apache Airflow? (y/n)"
    read -r response

    if [[ "$response" == "y" ]]; then
        echo "Configurando Airflow..."
        export AIRFLOW_HOME=$(pwd)/airflow

        airflow db init

        echo ""
        echo "Creando usuario admin de Airflow..."
        echo "Usuario: admin"
        echo "Password: admin"

        airflow users create \
            --username admin \
            --firstname Admin \
            --lastname User \
            --role Admin \
            --email admin@example.com \
            --password admin

        cp modulo9-airflow-orchestration/dags/*.py airflow/dags/

        cat > start_airflow.sh << 'EOF'
#!/bin/bash
echo "Iniciando Airflow..."
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow

echo "Iniciando Airflow Webserver en http://localhost:8080"
echo "Usuario: admin, Password: admin"
echo ""

airflow webserver --port 8080 &
sleep 5
airflow scheduler &

echo "Airflow iniciado. Presiona Ctrl+C para detener."
wait
EOF

        chmod +x start_airflow.sh
        echo "✓ Airflow configurado (./start_airflow.sh)"
    else
        echo "Airflow no configurado"
    fi
}

create_test_script() {
    echo ""
    echo "Creando script de prueba..."

    cat > test_setup.py << 'EOF'
import sys

def test_imports():
    packages = [
        'mlflow',
        'sklearn',
        'tensorflow',
        'torch',
        'pyspark',
        'pandas',
        'numpy',
        'matplotlib'
    ]

    failed = []

    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            failed.append(package)

    if failed:
        print(f"\nPaquetes faltantes: {', '.join(failed)}")
        return False
    else:
        print("\n✓ Todos los paquetes instalados correctamente")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
EOF

    echo "✓ Script de prueba creado"
}

run_tests() {
    echo ""
    echo "Ejecutando pruebas de configuración..."
    python test_setup.py

    if [ $? -eq 0 ]; then
        echo "✓ Configuración exitosa"
    else
        echo "✗ Algunos paquetes no se pudieron importar"
    fi
}

print_next_steps() {
    echo ""
    echo "========================================="
    echo "Configuración Completa!"
    echo "========================================="
    echo ""
    echo "Próximos pasos:"
    echo ""
    echo "1. Iniciar MLflow Tracking Server:"
    echo "   ./start_mlflow.sh"
    echo ""
    echo "2. Abrir MLflow UI en tu navegador:"
    echo "   http://localhost:5000"
    echo ""
    echo "3. (Opcional) Iniciar Airflow:"
    echo "   ./start_airflow.sh"
    echo ""
    echo "4. Empezar con los notebooks:"
    echo "   cd modulo1-sklearn"
    echo "   jupyter notebook"
    echo ""
    echo "Consulta GETTING_STARTED.md para más información"
    echo ""
}

main() {
    if ! check_python; then
        exit 1
    fi

    create_venv
    activate_venv
    install_dependencies || exit 1
    create_directories
    setup_mlflow
    setup_airflow
    create_test_script
    run_tests
    print_next_steps
}

main
