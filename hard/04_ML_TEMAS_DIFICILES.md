# Conocimientos Técnicos Difíciles: Machine Learning Engineering

## Objetivo
Temas complejos del día a día de ML engineering que un arquitecto debe dominar para apoyar efectivamente a científicos de datos y ML engineers.

---

## CATEGORÍA 1: Model Training y Optimization

### 1.1 Distributed Training
**Dificultad:** ⭐⭐⭐⭐⭐

**PyTorch Distributed Data Parallel (DDP)**

```python
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

# 1. Setup distributed environment
def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'

    # Initialize process group
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()

# 2. Wrap model con DDP
def train_ddp(rank, world_size):
    setup(rank, world_size)

    # Model en GPU específico
    model = YourModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    # Sampler distribuido
    train_sampler = DistributedSampler(
        train_dataset,
        num_replicas=world_size,
        rank=rank,
        shuffle=True
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        sampler=train_sampler,
        num_workers=4,
        pin_memory=True
    )

    optimizer = torch.optim.AdamW(ddp_model.parameters(), lr=1e-4)

    for epoch in range(num_epochs):
        # Importante: set epoch para shuffling
        train_sampler.set_epoch(epoch)

        for batch in train_loader:
            optimizer.zero_grad()

            # Forward pass
            outputs = ddp_model(batch['input'].to(rank))
            loss = criterion(outputs, batch['target'].to(rank))

            # Backward pass (gradients se promedian automáticamente)
            loss.backward()
            optimizer.step()

        # Solo rank 0 guarda checkpoint
        if rank == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': ddp_model.module.state_dict(),
                'optimizer_state_dict': optimizer.state_dict()
            }, f'checkpoint_epoch_{epoch}.pt')

    cleanup()

# 3. Launch con torch.multiprocessing
import torch.multiprocessing as mp

if __name__ == '__main__':
    world_size = torch.cuda.device_count()
    mp.spawn(
        train_ddp,
        args=(world_size,),
        nprocs=world_size,
        join=True
    )

# 4. Mixed Precision Training (speedup 2-3x)
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in train_loader:
    optimizer.zero_grad()

    # Forward en mixed precision
    with autocast():
        outputs = model(inputs)
        loss = criterion(outputs, targets)

    # Backward con gradient scaling
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

# 5. Gradient Accumulation (simular batch size mayor)
accumulation_steps = 4

for i, batch in enumerate(train_loader):
    outputs = model(inputs)
    loss = criterion(outputs, targets)

    # Normalizar loss
    loss = loss / accumulation_steps
    loss.backward()

    # Solo hacer step cada N iteraciones
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# 6. DeepSpeed para modelos gigantes
import deepspeed

# deepspeed_config.json
{
    "train_batch_size": 256,
    "gradient_accumulation_steps": 4,
    "optimizer": {
        "type": "AdamW",
        "params": {
            "lr": 1e-4
        }
    },
    "fp16": {
        "enabled": true
    },
    "zero_optimization": {
        "stage": 2,  # ZeRO-2: partition optimizer states
        "offload_optimizer": {
            "device": "cpu"
        }
    }
}

# Training code
model_engine, optimizer, _, _ = deepspeed.initialize(
    model=model,
    model_parameters=model.parameters(),
    config='deepspeed_config.json'
)

for batch in train_loader:
    loss = model_engine(batch)
    model_engine.backward(loss)
    model_engine.step()
```

---

### 1.2 Hyperparameter Tuning
**Dificultad:** ⭐⭐⭐⭐

```python
# 1. Optuna - Bayesian optimization
import optuna

def objective(trial):
    # Sugerir hyperparameters
    lr = trial.suggest_float('lr', 1e-5, 1e-1, log=True)
    batch_size = trial.suggest_categorical('batch_size', [16, 32, 64, 128])
    dropout = trial.suggest_float('dropout', 0.1, 0.5)
    hidden_size = trial.suggest_int('hidden_size', 128, 512, step=64)

    # Entrenar modelo
    model = create_model(
        hidden_size=hidden_size,
        dropout=dropout
    )

    train_loader = DataLoader(dataset, batch_size=batch_size)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # Training loop...
    val_loss = train_and_evaluate(model, train_loader, optimizer)

    return val_loss

# Crear study
study = optuna.create_study(
    direction='minimize',
    pruner=optuna.pruners.MedianPruner(),  # Early stopping de trials malos
    sampler=optuna.samplers.TPESampler()   # Bayesian optimization
)

# Optimizar
study.optimize(objective, n_trials=100, timeout=3600)

# Mejores parámetros
print("Best params:", study.best_params)
print("Best value:", study.best_value)

# Visualizar
import optuna.visualization as vis
vis.plot_optimization_history(study)
vis.plot_param_importances(study)

# 2. Ray Tune - Distributed hyperparameter tuning
from ray import tune
from ray.tune.schedulers import ASHAScheduler

def train_model(config):
    model = create_model(
        lr=config['lr'],
        hidden_size=config['hidden_size']
    )

    for epoch in range(10):
        # Training...
        val_loss = train_epoch(model)

        # Report intermediate result
        tune.report(loss=val_loss, epoch=epoch)

# Configurar búsqueda
config = {
    'lr': tune.loguniform(1e-5, 1e-1),
    'hidden_size': tune.choice([128, 256, 512]),
    'batch_size': tune.choice([16, 32, 64])
}

# Scheduler para early stopping
scheduler = ASHAScheduler(
    max_t=10,
    grace_period=1,
    reduction_factor=2
)

# Run tuning
analysis = tune.run(
    train_model,
    config=config,
    num_samples=100,
    scheduler=scheduler,
    resources_per_trial={'gpu': 1}
)

# Best config
best_config = analysis.get_best_config(metric='loss', mode='min')

# 3. Weights & Biases Sweeps
import wandb

# sweep_config.yaml
sweep_config = {
    'method': 'bayes',  # random, grid, bayes
    'metric': {
        'name': 'val_loss',
        'goal': 'minimize'
    },
    'parameters': {
        'lr': {
            'distribution': 'log_uniform_values',
            'min': 1e-5,
            'max': 1e-1
        },
        'batch_size': {
            'values': [16, 32, 64, 128]
        },
        'dropout': {
            'distribution': 'uniform',
            'min': 0.1,
            'max': 0.5
        }
    }
}

def train():
    with wandb.init() as run:
        config = wandb.config

        model = create_model(
            lr=config.lr,
            dropout=config.dropout
        )

        # Training...
        for epoch in range(epochs):
            train_loss = train_epoch(model)
            val_loss = validate(model)

            wandb.log({
                'epoch': epoch,
                'train_loss': train_loss,
                'val_loss': val_loss
            })

# Create sweep
sweep_id = wandb.sweep(sweep_config, project='my-project')

# Run agents
wandb.agent(sweep_id, function=train, count=100)
```

---

## CATEGORÍA 2: Model Serving

### 2.1 Model Optimization for Production
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# 1. Quantization (reducir de FP32 a INT8)
import torch
from torch.quantization import quantize_dynamic, quantize_static

# Dynamic quantization (fácil, sin calibration data)
model_fp32 = torch.load('model.pth')
model_int8 = quantize_dynamic(
    model_fp32,
    {torch.nn.Linear, torch.nn.LSTM},
    dtype=torch.qint8
)

# Tamaño reducido 4x, speedup 2-4x
torch.save(model_int8.state_dict(), 'model_int8.pth')

# Static quantization (mejor accuracy, necesita calibration)
model.eval()
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')

# Prepare
model_prepared = torch.quantization.prepare(model)

# Calibrate con representative data
with torch.no_grad():
    for batch in calibration_dataloader:
        model_prepared(batch)

# Convert
model_quantized = torch.quantization.convert(model_prepared)

# 2. ONNX Export (cross-framework compatibility)
import torch.onnx

# Export a ONNX
dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    export_params=True,
    opset_version=11,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)

# Optimizar ONNX
import onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic

quantize_dynamic(
    'model.onnx',
    'model_quantized.onnx',
    weight_type=QuantType.QInt8
)

# Inference con ONNX Runtime
session = ort.InferenceSession('model_quantized.onnx')

outputs = session.run(
    None,
    {'input': input_data.numpy()}
)

# 3. TorchScript (PyTorch production format)
# Tracing
model.eval()
example_input = torch.randn(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)

# Save
traced_model.save('model_traced.pt')

# Load en C++/producción
loaded_model = torch.jit.load('model_traced.pt')

# Scripting (para control flow)
scripted_model = torch.jit.script(model)

# 4. TensorRT (NVIDIA GPU optimization)
import tensorrt as trt

# Convert ONNX to TensorRT
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(TRT_LOGGER)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser = trt.OnnxParser(network, TRT_LOGGER)

# Parse ONNX
with open('model.onnx', 'rb') as f:
    parser.parse(f.read())

# Build engine
config = builder.create_builder_config()
config.max_workspace_size = 1 << 30  # 1GB

# FP16 precision
if builder.platform_has_fast_fp16:
    config.set_flag(trt.BuilderFlag.FP16)

engine = builder.build_engine(network, config)

# Serialize
with open('model.trt', 'wb') as f:
    f.write(engine.serialize())

# Inference
import pycuda.driver as cuda
import pycuda.autoinit

# Load engine
with open('model.trt', 'rb') as f:
    engine = trt.Runtime(TRT_LOGGER).deserialize_cuda_engine(f.read())

context = engine.create_execution_context()

# Allocate buffers
inputs, outputs, bindings, stream = allocate_buffers(engine)

# Run inference
trt_outputs = do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream)
```

---

### 2.2 Model Serving Infrastructure
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# 1. FastAPI Model Server
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import torch
from PIL import Image
import io

app = FastAPI()

# Load model al startup
model = None

@app.on_event("startup")
async def load_model():
    global model
    model = torch.jit.load('model_traced.pt')
    model.eval()

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    # Preprocess
    inputs = preprocess(request.text)

    # Inference
    with torch.no_grad():
        outputs = model(inputs)
        prediction = outputs.argmax().item()
        confidence = outputs.softmax(dim=-1).max().item()

    return PredictionResponse(
        prediction=prediction,
        confidence=confidence
    )

# Image upload endpoint
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Preprocess
    inputs = transform(image).unsqueeze(0)

    # Inference
    with torch.no_grad():
        outputs = model(inputs)

    return {"class": outputs.argmax().item()}

# Batch prediction
@app.post("/predict-batch")
async def predict_batch(requests: List[PredictionRequest]):
    # Batch inputs
    inputs = torch.stack([preprocess(r.text) for r in requests])

    # Batch inference
    with torch.no_grad():
        outputs = model(inputs)

    return [
        {"prediction": o.argmax().item()}
        for o in outputs
    ]

# 2. TorchServe (PyTorch production server)
# model_handler.py
from ts.torch_handler.base_handler import BaseHandler

class CustomHandler(BaseHandler):
    def initialize(self, context):
        self.manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")

        # Load model
        self.model = torch.jit.load(f'{model_dir}/model.pt')
        self.model.eval()

    def preprocess(self, data):
        # Process input
        images = []
        for row in data:
            image = row.get("data") or row.get("body")
            image = Image.open(io.BytesIO(image))
            image = self.transform(image)
            images.append(image)

        return torch.stack(images)

    def inference(self, data):
        with torch.no_grad():
            return self.model(data)

    def postprocess(self, data):
        return data.argmax(dim=1).tolist()

# Package model
torch-model-archiver \
    --model-name resnet50 \
    --version 1.0 \
    --serialized-file model.pt \
    --handler model_handler.py \
    --export-path model_store

# Start server
torchserve \
    --start \
    --model-store model_store \
    --models resnet50=resnet50.mar \
    --ncs

# 3. Triton Inference Server (multi-framework)
# config.pbtxt
name: "my_model"
platform: "pytorch_libtorch"
max_batch_size: 32

input [
  {
    name: "input"
    data_type: TYPE_FP32
    dims: [ 3, 224, 224 ]
  }
]

output [
  {
    name: "output"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]

dynamic_batching {
  preferred_batch_size: [ 8, 16, 32 ]
  max_queue_delay_microseconds: 5000
}

# Python client
import tritonclient.http as httpclient

client = httpclient.InferenceServerClient(url="localhost:8000")

# Prepare input
inputs = httpclient.InferInput("input", input_data.shape, "FP32")
inputs.set_data_from_numpy(input_data)

outputs = httpclient.InferRequestedOutput("output")

# Inference
results = client.infer(
    model_name="my_model",
    inputs=[inputs],
    outputs=[outputs]
)

output_data = results.as_numpy("output")

# 4. Model caching y warmup
import functools
from collections import OrderedDict

class ModelCache:
    def __init__(self, max_size=5):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get(self, model_version):
        if model_version in self.cache:
            # Move to end (LRU)
            self.cache.move_to_end(model_version)
            return self.cache[model_version]
        return None

    def put(self, model_version, model):
        if len(self.cache) >= self.max_size:
            # Remove oldest
            self.cache.popitem(last=False)

        self.cache[model_version] = model

# Warmup
def warmup_model(model, input_shape, num_iterations=10):
    dummy_input = torch.randn(input_shape)

    with torch.no_grad():
        for _ in range(num_iterations):
            _ = model(dummy_input)

    print("Model warmed up!")
```

---

## CATEGORÍA 3: MLOps y Monitoring

### 3.1 Experiment Tracking
**Dificultad:** ⭐⭐⭐⭐

```python
# 1. MLflow
import mlflow
import mlflow.pytorch

# Start run
with mlflow.start_run(run_name="experiment_1"):
    # Log parameters
    mlflow.log_param("lr", 0.001)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 10)

    # Training loop
    for epoch in range(epochs):
        train_loss = train_epoch(model)
        val_loss = validate(model)

        # Log metrics
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)

    # Log model
    mlflow.pytorch.log_model(model, "model")

    # Log artifacts
    mlflow.log_artifact("config.yaml")
    mlflow.log_artifact("training_plot.png")

# Load model
model_uri = "runs:/<run_id>/model"
loaded_model = mlflow.pytorch.load_model(model_uri)

# 2. Weights & Biases
import wandb

# Initialize
wandb.init(
    project="my-project",
    config={
        "lr": 0.001,
        "batch_size": 32,
        "epochs": 10
    }
)

# Training loop
for epoch in range(epochs):
    for batch in train_loader:
        # Training step...

        # Log
        wandb.log({
            "train_loss": loss.item(),
            "learning_rate": optimizer.param_groups[0]['lr'],
            "epoch": epoch
        })

    # Log images
    wandb.log({
        "predictions": wandb.Image(
            image,
            caption=f"Pred: {pred}, True: {true}"
        )
    })

    # Log confusion matrix
    wandb.log({
        "confusion_matrix": wandb.plot.confusion_matrix(
            y_true=y_true,
            preds=preds,
            class_names=class_names
        )
    })

# Save model
wandb.save('model.h5')

# Finish
wandb.finish()

# 3. TensorBoard
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment1')

# Log scalars
writer.add_scalar('Loss/train', train_loss, epoch)
writer.add_scalar('Loss/val', val_loss, epoch)

# Log images
writer.add_image('predictions', img_grid, epoch)

# Log model graph
writer.add_graph(model, input_sample)

# Log hyperparameters
writer.add_hparams(
    {'lr': 0.001, 'batch_size': 32},
    {'val_loss': val_loss, 'val_acc': val_acc}
)

writer.close()
```

---

### 3.2 Model Monitoring in Production
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# 1. Data Drift Detection
from scipy import stats
import numpy as np

class DriftDetector:
    def __init__(self, reference_data):
        self.reference_data = reference_data
        self.reference_stats = self.compute_stats(reference_data)

    def compute_stats(self, data):
        return {
            'mean': np.mean(data, axis=0),
            'std': np.std(data, axis=0),
            'quantiles': np.quantile(data, [0.25, 0.5, 0.75], axis=0)
        }

    def detect_drift(self, new_data, threshold=0.05):
        # Kolmogorov-Smirnov test
        drifts = []
        for i in range(new_data.shape[1]):
            statistic, p_value = stats.ks_2samp(
                self.reference_data[:, i],
                new_data[:, i]
            )

            if p_value < threshold:
                drifts.append({
                    'feature': i,
                    'p_value': p_value,
                    'statistic': statistic
                })

        return drifts

# Uso
detector = DriftDetector(training_data)
drifts = detector.detect_drift(production_data)

if drifts:
    print(f"Drift detected in {len(drifts)} features!")
    # Trigger retraining

# 2. Model Performance Monitoring
class ModelMonitor:
    def __init__(self):
        self.predictions = []
        self.ground_truth = []
        self.latencies = []

    def log_prediction(self, input_data, prediction, latency):
        self.predictions.append(prediction)
        self.latencies.append(latency)

        # Store input features para drift detection
        self.store_features(input_data)

    def log_ground_truth(self, prediction_id, actual):
        self.ground_truth.append(actual)

    def compute_metrics(self):
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support

        accuracy = accuracy_score(self.ground_truth, self.predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            self.ground_truth,
            self.predictions,
            average='weighted'
        )

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'avg_latency': np.mean(self.latencies),
            'p95_latency': np.percentile(self.latencies, 95),
            'p99_latency': np.percentile(self.latencies, 99)
        }

# 3. Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Counters
prediction_counter = Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_version', 'class']
)

error_counter = Counter(
    'model_errors_total',
    'Total errors',
    ['model_version', 'error_type']
)

# Histogram
latency_histogram = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency',
    ['model_version']
)

# Gauge
model_accuracy = Gauge(
    'model_accuracy',
    'Current model accuracy',
    ['model_version']
)

# Instrumentar predicción
@latency_histogram.labels(model_version='v1').time()
def predict(input_data):
    try:
        prediction = model(input_data)
        prediction_counter.labels(
            model_version='v1',
            class=prediction
        ).inc()
        return prediction
    except Exception as e:
        error_counter.labels(
            model_version='v1',
            error_type=type(e).__name__
        ).inc()
        raise

# 4. Logging estructurado
import logging
import json

logger = logging.getLogger('model_inference')

def log_prediction(input_data, prediction, confidence, latency):
    log_data = {
        'event': 'prediction',
        'model_version': 'v1',
        'prediction': prediction,
        'confidence': confidence,
        'latency_ms': latency * 1000,
        'input_features': {
            'feature1': input_data[0],
            'feature2': input_data[1]
        }
    }

    logger.info(json.dumps(log_data))

    # Alertar si confidence baja
    if confidence < 0.7:
        logger.warning(
            f"Low confidence prediction: {confidence}",
            extra={'prediction_data': log_data}
        )
```

---

## Resumen Prioridades ML

| Tema | Dificultad | Criticidad | Frecuencia | Prioridad |
|------|------------|------------|------------|-----------|
| Distributed Training | 5 | 4 | 3 | **ALTA** |
| Model Optimization | 5 | 5 | 4 | **CRÍTICA** |
| Model Serving | 5 | 5 | 5 | **CRÍTICA** |
| Hyperparameter Tuning | 4 | 4 | 4 | **ALTA** |
| MLOps Monitoring | 5 | 5 | 5 | **CRÍTICA** |
| Data Drift Detection | 4 | 4 | 3 | **ALTA** |
