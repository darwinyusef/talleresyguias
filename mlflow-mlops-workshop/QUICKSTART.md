# ⚡ QuickStart - MLflow MLOps Workshop

## Inicio en 5 Minutos

### 1. Instalación Automática

```bash
cd mlflow-mlops-workshop
chmod +x setup.sh
./setup.sh
```

El script instalará automáticamente:
- Entorno virtual Python
- Todas las dependencias (MLflow, TensorFlow, PyTorch, Spark, etc.)
- Configuración de Airflow (opcional)
- Scripts de inicio

**Tiempo estimado**: 10-15 minutos

### 2. Iniciar MLflow

```bash
./start_mlflow.sh
```

Abre tu navegador en: **http://localhost:5000**

### 3. Primer Experimento

```bash
source venv/bin/activate
cd modulo1-sklearn
jupyter notebook 01_mlflow_basics.ipynb
```

Ejecuta todas las celdas (Cell → Run All)

### 4. Ver Resultados

Ve a **http://localhost:5000** y verás:
- Tu primer experimento "sklearn-basics"
- Múltiples runs con diferentes modelos
- Métricas, parámetros y artefactos

---

## Roadmap de 3 Días

### 📅 Día 1: Fundamentos (4-5 horas)

**Mañana (2h)**:
```bash
cd modulo1-sklearn
jupyter notebook 01_mlflow_basics.ipynb
```
- Aprende conceptos básicos de MLflow
- Logging de parámetros y métricas
- Guardar y cargar modelos

**Tarde (2-3h)**:
```bash
jupyter notebook 02_classification_pipeline.ipynb
jupyter notebook 03_regression_advanced.ipynb
```
- Pipelines de ML
- Comparación de modelos
- Regularización

**Resultado**: Dominas MLflow tracking básico

---

### 📅 Día 2: Deep Learning (6-7 horas)

**Mañana (3-4h)**:
```bash
cd modulo2-tensorflow
jupyter notebook 01_cnn_image_classification.ipynb
```
- CNNs con TensorFlow
- Custom callbacks
- Tracking de DL

**Tarde (3h)**:
```bash
jupyter notebook 02_rnn_time_series.ipynb
```
- LSTM para series temporales
- Multi-step forecasting

**Opcional (2h)**:
```bash
cd modulo3-pytorch
jupyter notebook 01_pytorch_basics_mlflow.ipynb
```
- PyTorch con MLflow
- Custom training loops

**Resultado**: Sabes trackear modelos de Deep Learning

---

### 📅 Día 3: Producción (5-6 horas)

**Mañana (2-3h)**:
```bash
cd modulo7-spark-mlflow
jupyter notebook 01_spark_ml_basics.ipynb
```
- ML distribuido con Spark
- CrossValidation en cluster

**Tarde (3h)**:
```bash
cd modulo9-airflow-orchestration

./start_airflow.sh

```

Abre **http://localhost:8080** (user: admin, pass: admin)
- Activa el DAG `ml_training_pipeline`
- Observa la ejecución
- Revisa resultados en MLflow

**Resultado**: Puedes orquestar pipelines ML de producción

---

## Comandos Útiles

### MLflow

```bash
mlflow ui
mlflow experiments list
mlflow runs list --experiment-id 0

mlflow models serve -m runs:/<RUN_ID>/model -p 5001
```

### Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow

airflow dags list
airflow dags trigger ml_training_pipeline
airflow dags unpause ml_training_pipeline

airflow tasks list ml_training_pipeline
```

### Jupyter

```bash
jupyter notebook
jupyter notebook list

jupyter nbconvert --to html notebook.ipynb
```

### Spark

```bash
pyspark
spark-submit script.py

$SPARK_HOME/bin/spark-shell
```

---

## Troubleshooting Rápido

### Error: "MLflow UI not loading"
```bash
pkill -f "mlflow"
./start_mlflow.sh
```

### Error: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "CUDA not available" (para GPU)
```bash
python -c "import torch; print(torch.cuda.is_available())"
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Error: "Airflow webserver won't start"
```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db reset  # ⚠️ Borra todos los DAG runs
airflow db init
```

---

## Primeros Pasos Recomendados

1. **Lee GETTING_STARTED.md** para setup detallado
2. **Ejecuta modulo1** para fundamentos
3. **Explora MLflow UI** familiarízate con la interfaz
4. **Revisa CONTENIDO_COMPLETO.md** para ver todo el contenido
5. **Experimenta** modifica notebooks y observa cambios

---

## Recursos de Aprendizaje

### Documentación Oficial
- [MLflow Docs](https://mlflow.org/docs/latest/index.html)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)

### Tutoriales Rápidos
- [MLflow Quickstart (5 min)](https://mlflow.org/docs/latest/quickstart.html)
- [MLflow Tutorials](https://mlflow.org/docs/latest/tutorials-and-examples/index.html)

### Videos
- [MLflow Overview](https://www.youtube.com/watch?v=859OxXrt_TI)
- [MLflow in Production](https://www.youtube.com/watch?v=9hF7IXF8gVs)

---

## Arquitectura del Taller

```
Tu Laptop
├── MLflow Tracking Server (localhost:5000)
│   └── SQLite Backend (mlflow.db)
├── Airflow (localhost:8080)
│   ├── Webserver
│   ├── Scheduler
│   └── DAGs
├── Jupyter Notebooks
│   └── 8 notebooks interactivos
└── Spark (cuando se use)
    └── Local mode
```

---

## Checklist de Completitud

Marca conforme avanzas:

### Fundamentos
- [ ] MLflow instalado y corriendo
- [ ] Primer experimento ejecutado
- [ ] MLflow UI explorado
- [ ] Modelo guardado y cargado

### Intermedio
- [ ] Pipeline de clasificación completado
- [ ] CNN entrenada
- [ ] Serie temporal forecasted
- [ ] Modelos comparados

### Avanzado
- [ ] PyTorch integrado con MLflow
- [ ] Spark + MLflow ejecutado
- [ ] Airflow DAG corrido
- [ ] Batch predictions realizadas

---

## Próximos Pasos

Después de completar el taller:

1. **Aplica a tu proyecto**: Usa MLflow en tu trabajo actual
2. **Cloud deployment**: Despliega MLflow en AWS/Azure/GCP
3. **CI/CD**: Integra con GitHub Actions
4. **Contribuye**: Mejora este taller con PRs
5. **Comparte**: Enseña MLflow a tu equipo

---

## Support

Si tienes problemas:
1. Revisa **Troubleshooting** arriba
2. Consulta **GETTING_STARTED.md**
3. Lee **CONTENIDO_COMPLETO.md**
4. Busca en [MLflow GitHub Issues](https://github.com/mlflow/mlflow/issues)

---

## Un Último Consejo

**No te apresures.** Este taller tiene 15-20 horas de contenido.

Tómate tu tiempo para:
- Entender la teoría
- Experimentar con el código
- Hacer preguntas
- Modificar y probar

**La práctica hace al maestro en MLOps.**

¡Buena suerte y disfruta el taller! 🚀

---

**¿Listo para empezar?**

```bash
./setup.sh && ./start_mlflow.sh
```
