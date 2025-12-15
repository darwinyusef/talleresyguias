# Técnicas de Machine Learning para Desarrolladores 2026
## ML Práctico en Producción - De Zero a Hero

**Versión:** 1.0
**Fecha:** 2024-12-03
**Audiencia:** Desarrolladores Backend/Frontend que quieren integrar ML real

---

## 📋 Índice

1. [ML para Desarrolladores vs ML Research](#intro)
2. [Stack Tecnológico 2026](#stack)
3. [Técnicas Esenciales](#tecnicas)
4. [MLOps Práctico](#mlops)
5. [Casos de Uso Reales](#casos-uso)
6. [Deployment Patterns](#deployment)
7. [Debugging y Monitoring](#debugging)
8. [Roadmap de Aprendizaje](#roadmap)

---

## 1. ML PARA DESARROLLADORES VS ML RESEARCH {#intro}

### 1.1 Diferencias Clave

| Aspecto | ML Research | ML en Producción |
|---------|-------------|------------------|
| **Objetivo** | Mejorar accuracy 0.1% | Sistema funcionando 24/7 |
| **Métricas** | Accuracy, F1, AUC | Latencia, throughput, costo |
| **Código** | Jupyter notebooks | APIs, microservicios |
| **Datos** | Datasets limpios | Datos sucios, streaming |
| **Reproducibilidad** | Paper con resultados | CI/CD, versionado |
| **Foco** | Modelo | Sistema completo |

### 1.2 Skills que Necesitas como Desarrollador

**Sí necesitas:**
- ✅ Usar modelos pre-entrenados (transfer learning)
- ✅ Fine-tuning básico
- ✅ Feature engineering
- ✅ Deployment de modelos
- ✅ Monitoreo de predicciones
- ✅ A/B testing

**NO necesitas (al principio):**
- ❌ Crear arquitecturas nuevas de redes neuronales
- ❌ Publicar papers
- ❌ Entender matemáticas avanzadas de optimización
- ❌ Implementar backpropagation desde cero

---

## 2. STACK TECNOLÓGICO 2026 {#stack}

### 2.1 Stack Completo

```
┌─────────────────────────────────────────────────────┐
│              ML STACK 2026                          │
├─────────────────────────────────────────────────────┤
│ TRAINING                                            │
│  - PyTorch 2.x (primary)                           │
│  - JAX (high performance)                          │
│  - Lightning (PyTorch wrapper)                     │
├─────────────────────────────────────────────────────┤
│ DATA                                                │
│  - DuckDB (analytics)                              │
│  - Polars (fast dataframes)                        │
│  - Arrow (interchange format)                      │
├─────────────────────────────────────────────────────┤
│ DEPLOYMENT                                          │
│  - ONNX Runtime (inference)                        │
│  - TorchServe (PyTorch models)                     │
│  - Triton (NVIDIA, multi-framework)                │
├─────────────────────────────────────────────────────┤
│ MLOPS                                               │
│  - MLflow (tracking)                               │
│  - DVC (data versioning)                           │
│  - Weights & Biases (experiments)                  │
│  - Evidently AI (monitoring)                       │
├─────────────────────────────────────────────────────┤
│ INFRASTRUCTURE                                      │
│  - Kubernetes (orchestration)                      │
│  - KServe (model serving)                          │
│  - Ray (distributed)                               │
└─────────────────────────────────────────────────────┘
```

### 2.2 Instalación Rápida

```bash
# Ambiente base
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Data processing
pip install polars duckdb pyarrow

# Training utilities
pip install lightning transformers datasets accelerate

# Deployment
pip install onnx onnxruntime fastapi uvicorn

# MLOps
pip install mlflow wandb dvc evidently

# Monitoring
pip install prometheus-client opentelemetry-api
```

---

## 3. TÉCNICAS ESENCIALES {#tecnicas}

### 3.1 Transfer Learning ⭐⭐⭐⭐⭐

**Concepto:** Usar modelos pre-entrenados y adaptarlos a tu problema.

**Cuándo usar:**
- ✅ Tienes pocos datos (< 10k ejemplos)
- ✅ Problema similar a uno ya resuelto
- ✅ Quieres resultados rápidos

**Ejemplo: Clasificación de Imágenes**

```python
# transfer_learning/image_classifier.py
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os

class CustomImageDataset(Dataset):
    """Dataset custom para tus imágenes"""
    def __init__(self, image_dir, labels, transform=None):
        self.image_dir = image_dir
        self.labels = labels
        self.transform = transform
        self.image_files = os.listdir(image_dir)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_files[idx])
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

def create_transfer_learning_model(num_classes, freeze_backbone=True):
    """
    Crear modelo con transfer learning desde ResNet50

    Args:
        num_classes: Número de clases de tu problema
        freeze_backbone: Si True, solo entrena la última capa
    """
    # Cargar modelo pre-entrenado
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

    # Congelar capas del backbone (opcional)
    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False

    # Reemplazar última capa para tu problema
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes)
    )

    return model

def train_transfer_learning_model(
    model,
    train_loader,
    val_loader,
    num_epochs=10,
    learning_rate=0.001,
    device='cuda'
):
    """Entrenar modelo con transfer learning"""

    model = model.to(device)

    # Optimizer: learning rate más alto para última capa
    backbone_params = [p for n, p in model.named_parameters() if 'fc' not in n and p.requires_grad]
    head_params = [p for n, p in model.named_parameters() if 'fc' in n]

    optimizer = torch.optim.AdamW([
        {'params': backbone_params, 'lr': learning_rate * 0.1},  # Backbone: LR bajo
        {'params': head_params, 'lr': learning_rate}  # Head: LR normal
    ])

    criterion = nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, num_epochs)

    best_val_acc = 0.0

    for epoch in range(num_epochs):
        # Training
        model.train()
        train_loss = 0.0
        train_correct = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            train_correct += (predicted == labels).sum().item()

        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                val_correct += (predicted == labels).sum().item()

        train_acc = train_correct / len(train_loader.dataset)
        val_acc = val_correct / len(val_loader.dataset)

        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"  Train Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.4f}")
        print(f"  Val Loss: {val_loss/len(val_loader):.4f}, Acc: {val_acc:.4f}")

        # Guardar mejor modelo
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')
            print(f"  ✓ New best model saved! Val Acc: {val_acc:.4f}")

        scheduler.step()

    return model

# Uso
if __name__ == "__main__":
    # Transforms
    train_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Dataset
    train_dataset = CustomImageDataset('data/train', labels, transform=train_transform)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

    # Modelo
    model = create_transfer_learning_model(num_classes=10)

    # Entrenar
    model = train_transfer_learning_model(model, train_loader, val_loader)
```

---

### 3.2 Few-Shot Learning ⭐⭐⭐⭐⭐

**Concepto:** Aprender con muy pocos ejemplos (5-100 por clase).

**Técnicas:**
- **Prompting**: Para LLMs (GPT, Claude)
- **Metric Learning**: Redes siamesas
- **Meta-Learning**: MAML, Prototypical Networks

**Ejemplo: Few-Shot Classification con Sentence Transformers**

```python
# few_shot/text_classifier.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class FewShotTextClassifier:
    """
    Clasificador few-shot usando embeddings de SentenceTransformers

    Funciona con tan solo 5 ejemplos por clase!
    """

    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.class_embeddings = {}
        self.classes = []

    def fit(self, examples: Dict[str, List[str]]):
        """
        Entrenar con pocos ejemplos

        Args:
            examples: {"clase1": ["ejemplo1", "ejemplo2"], "clase2": [...]}
        """
        self.classes = list(examples.keys())

        for class_name, texts in examples.items():
            # Generar embeddings para cada clase
            embeddings = self.model.encode(texts)

            # Usar el centroid (promedio) de todos los ejemplos
            class_embedding = np.mean(embeddings, axis=0)
            self.class_embeddings[class_name] = class_embedding

        print(f"Trained with {len(self.classes)} classes")
        for cls, texts in examples.items():
            print(f"  {cls}: {len(texts)} examples")

    def predict(self, text: str, return_scores=False):
        """Predecir clase de un texto"""
        # Generar embedding del texto
        text_embedding = self.model.encode([text])[0]

        # Calcular similitud con cada clase
        scores = {}
        for class_name, class_embedding in self.class_embeddings.items():
            similarity = cosine_similarity(
                [text_embedding],
                [class_embedding]
            )[0][0]
            scores[class_name] = similarity

        # Mejor match
        predicted_class = max(scores, key=scores.get)

        if return_scores:
            return predicted_class, scores
        return predicted_class

    def predict_batch(self, texts: List[str]) -> List[str]:
        """Predicción en batch (más eficiente)"""
        embeddings = self.model.encode(texts)
        predictions = []

        for embedding in embeddings:
            scores = {}
            for class_name, class_embedding in self.class_embeddings.items():
                similarity = cosine_similarity(
                    [embedding],
                    [class_embedding]
                )[0][0]
                scores[class_name] = similarity

            predictions.append(max(scores, key=scores.get))

        return predictions

# Uso: Clasificar tickets de soporte con solo 5 ejemplos por clase
if __name__ == "__main__":
    # Solo 5 ejemplos por clase!
    examples = {
        "bug": [
            "The app crashes when I click submit",
            "Error 500 on login page",
            "Cannot save my profile, getting errors",
            "Application freezes after 5 minutes",
            "Button doesn't work on mobile"
        ],
        "feature_request": [
            "Can you add dark mode?",
            "Would love to see export to PDF",
            "Please add support for multiple languages",
            "Integration with Slack would be great",
            "Need bulk upload feature"
        ],
        "question": [
            "How do I reset my password?",
            "What are your business hours?",
            "Is there a mobile app available?",
            "How much does the pro plan cost?",
            "Can I export my data?"
        ]
    }

    # Entrenar
    classifier = FewShotTextClassifier()
    classifier.fit(examples)

    # Predecir
    test_texts = [
        "The button is broken and not responding",  # bug
        "Can you add a search feature?",  # feature_request
        "How do I upgrade my account?"  # question
    ]

    for text in test_texts:
        prediction, scores = classifier.predict(text, return_scores=True)
        print(f"\nText: {text}")
        print(f"Prediction: {prediction}")
        print(f"Scores: {scores}")
```

---

### 3.3 Online Learning / Incremental Learning ⭐⭐⭐⭐

**Concepto:** Modelo que aprende continuamente de nuevos datos.

**Cuándo usar:**
- ✅ Datos llegan en streaming
- ✅ Distribución de datos cambia (concept drift)
- ✅ No puedes re-entrenar desde cero frecuentemente

**Ejemplo: Sistema de Recomendaciones Online**

```python
# online_learning/recommender.py
from river import linear_model, preprocessing, compose, metrics
import numpy as np
from datetime import datetime
from typing import Dict, List

class OnlineRecommender:
    """
    Sistema de recomendaciones que aprende online
    Usa River library para online learning
    """

    def __init__(self, learning_rate=0.01):
        # Modelo online: aprende con cada nueva interacción
        self.model = compose.Pipeline(
            preprocessing.StandardScaler(),
            linear_model.LogisticRegression(
                optimizer=linear_model.optimizers.SGD(learning_rate)
            )
        )

        self.metric = metrics.ROCAUC()
        self.interactions = 0

    def extract_features(self, user_id: int, item_id: int, context: Dict) -> Dict:
        """Extraer features de la interacción"""
        features = {
            'user_id': user_id,
            'item_id': item_id,
            'hour': context.get('hour', 0),
            'day_of_week': context.get('day_of_week', 0),
            'user_activity_last_7d': context.get('user_activity_last_7d', 0),
            'item_popularity': context.get('item_popularity', 0),
            'user_item_affinity': context.get('user_item_affinity', 0.5)
        }
        return features

    def predict(self, user_id: int, item_id: int, context: Dict) -> float:
        """Predecir probabilidad de interacción"""
        features = self.extract_features(user_id, item_id, context)

        # Predecir probabilidad
        proba = self.model.predict_proba_one(features)
        return proba.get(True, 0.0)

    def learn(self, user_id: int, item_id: int, clicked: bool, context: Dict):
        """Aprender de una nueva interacción"""
        features = self.extract_features(user_id, item_id, context)

        # Actualizar modelo
        self.model.learn_one(features, clicked)

        # Actualizar métrica
        y_pred = self.model.predict_proba_one(features).get(True, 0.0)
        self.metric.update(clicked, y_pred)

        self.interactions += 1

        if self.interactions % 1000 == 0:
            print(f"Interactions: {self.interactions}, ROC-AUC: {self.metric.get():.4f}")

    def recommend(
        self,
        user_id: int,
        candidate_items: List[int],
        context: Dict,
        top_k: int = 10
    ) -> List[tuple]:
        """Recomendar top-k items"""
        scores = []

        for item_id in candidate_items:
            score = self.predict(user_id, item_id, context)
            scores.append((item_id, score))

        # Ordenar por score descendente
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_k]

# Simulación de sistema de recomendaciones
if __name__ == "__main__":
    recommender = OnlineRecommender()

    # Simular stream de interacciones
    for i in range(10000):
        # Datos sintéticos
        user_id = np.random.randint(0, 1000)
        item_id = np.random.randint(0, 5000)

        context = {
            'hour': datetime.now().hour,
            'day_of_week': datetime.now().weekday(),
            'user_activity_last_7d': np.random.randint(0, 100),
            'item_popularity': np.random.random(),
            'user_item_affinity': np.random.random()
        }

        # Simular si el usuario hizo click (mayor probabilidad si affinity alta)
        clicked = np.random.random() < context['user_item_affinity']

        # Aprender de la interacción
        recommender.learn(user_id, item_id, clicked, context)

    # Hacer recomendación
    recommendations = recommender.recommend(
        user_id=42,
        candidate_items=list(range(100)),
        context={'hour': 14, 'day_of_week': 2},
        top_k=5
    )

    print("\nTop 5 recommendations for user 42:")
    for item_id, score in recommendations:
        print(f"  Item {item_id}: {score:.4f}")
```

---

### 3.4 Model Distillation ⭐⭐⭐⭐

**Concepto:** Comprimir modelo grande (teacher) en modelo pequeño (student).

**Cuándo usar:**
- ✅ Necesitas baja latencia en producción
- ✅ Deployment en edge/mobile
- ✅ Reducir costos de inferencia

**Ejemplo: Destilación de BERT**

```python
# distillation/distill_bert.py
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel, BertTokenizer, BertConfig

class TeacherModel(nn.Module):
    """Modelo grande: BERT-base"""
    def __init__(self, num_classes):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.classifier = nn.Linear(768, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.classifier(outputs.pooler_output)
        return logits

class StudentModel(nn.Module):
    """Modelo pequeño: BERT-tiny (3 capas)"""
    def __init__(self, num_classes):
        super().__init__()
        config = BertConfig(
            hidden_size=256,
            num_hidden_layers=3,
            num_attention_heads=4,
            intermediate_size=1024
        )
        self.bert = BertModel(config)
        self.classifier = nn.Linear(256, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.classifier(outputs.pooler_output)
        return logits

def distillation_loss(student_logits, teacher_logits, labels, temperature=3.0, alpha=0.5):
    """
    Loss de distilación

    Args:
        temperature: Suaviza las probabilidades (mayor = más suave)
        alpha: Balance entre distillation loss y task loss
    """
    # Soft targets del teacher
    soft_targets = F.softmax(teacher_logits / temperature, dim=1)
    soft_student = F.log_softmax(student_logits / temperature, dim=1)

    # Distillation loss (KL divergence)
    distill_loss = F.kl_div(soft_student, soft_targets, reduction='batchmean')
    distill_loss = distill_loss * (temperature ** 2)

    # Task loss (cross entropy con labels reales)
    task_loss = F.cross_entropy(student_logits, labels)

    # Combinar
    total_loss = alpha * distill_loss + (1 - alpha) * task_loss

    return total_loss

def train_student(
    teacher_model,
    student_model,
    train_loader,
    num_epochs=5,
    device='cuda',
    temperature=3.0,
    alpha=0.7
):
    """Entrenar student con distillation"""

    teacher_model.eval()  # Teacher en modo eval
    student_model.train()

    optimizer = torch.optim.AdamW(student_model.parameters(), lr=2e-5)

    for epoch in range(num_epochs):
        total_loss = 0

        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            # Teacher predictions (sin gradientes)
            with torch.no_grad():
                teacher_logits = teacher_model(input_ids, attention_mask)

            # Student predictions
            student_logits = student_model(input_ids, attention_mask)

            # Calcular loss de distillation
            loss = distillation_loss(
                student_logits,
                teacher_logits,
                labels,
                temperature,
                alpha
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}")

    return student_model

# Comparar tamaños
def compare_models(teacher, student):
    """Comparar tamaño y velocidad"""
    teacher_params = sum(p.numel() for p in teacher.parameters())
    student_params = sum(p.numel() for p in student.parameters())

    print(f"\nModel Comparison:")
    print(f"Teacher: {teacher_params:,} parameters")
    print(f"Student: {student_params:,} parameters")
    print(f"Reduction: {(1 - student_params/teacher_params)*100:.1f}%")

    # Benchmark de velocidad
    import time

    dummy_input = torch.randint(0, 1000, (1, 128)).to('cuda')
    dummy_mask = torch.ones(1, 128).to('cuda')

    # Teacher
    teacher.eval()
    with torch.no_grad():
        start = time.time()
        for _ in range(100):
            teacher(dummy_input, dummy_mask)
        teacher_time = (time.time() - start) / 100

    # Student
    student.eval()
    with torch.no_grad():
        start = time.time()
        for _ in range(100):
            student(dummy_input, dummy_mask)
        student_time = (time.time() - start) / 100

    print(f"\nLatency:")
    print(f"Teacher: {teacher_time*1000:.2f}ms")
    print(f"Student: {student_time*1000:.2f}ms")
    print(f"Speedup: {teacher_time/student_time:.1f}x")
```

---

### 3.5 Data Augmentation ⭐⭐⭐⭐⭐

**Concepto:** Generar más datos de entrenamiento desde datos existentes.

**Técnicas por tipo de dato:**

**Imágenes:**
```python
# augmentation/image_aug.py
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2

# Augmentations fuertes para entrenamiento
train_transform = A.Compose([
    # Geométricas
    A.RandomRotate90(p=0.5),
    A.Flip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=15, p=0.5),

    # Espaciales
    A.GridDistortion(p=0.3),
    A.ElasticTransform(p=0.3),

    # Color
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(p=0.3),
    A.RGBShift(p=0.3),
    A.CLAHE(p=0.3),

    # Ruido
    A.GaussNoise(p=0.3),
    A.GaussianBlur(p=0.2),

    # Cutout
    A.CoarseDropout(max_holes=8, max_height=32, max_width=32, p=0.3),

    # Normalización
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

# Uso
image = cv2.imread('image.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
augmented = train_transform(image=image)['image']
```

**Texto (NLP):**
```python
# augmentation/text_aug.py
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas

class TextAugmenter:
    def __init__(self):
        # Back-translation augmentation
        self.back_trans = naw.BackTranslationAug(
            from_model_name='facebook/wmt19-en-de',
            to_model_name='facebook/wmt19-de-en'
        )

        # Synonym replacement
        self.synonym = naw.SynonymAug(aug_src='wordnet')

        # Contextual word embeddings
        self.context = naw.ContextualWordEmbsAug(
            model_path='bert-base-uncased',
            action="substitute"
        )

    def augment(self, text: str, num_aug: int = 3) -> list:
        """Generar variaciones de un texto"""
        augmented_texts = [text]  # Original

        # Back-translation
        try:
            aug_text = self.back_trans.augment(text)
            if aug_text != text:
                augmented_texts.append(aug_text)
        except:
            pass

        # Synonym replacement
        for _ in range(num_aug - 1):
            aug_text = self.synonym.augment(text)
            if aug_text != text:
                augmented_texts.append(aug_text)

        return augmented_texts[:num_aug + 1]

# Uso: Aumentar dataset de clasificación
augmenter = TextAugmenter()

original_texts = [
    "This product is amazing!",
    "Terrible customer service"
]

for text in original_texts:
    augmented = augmenter.augment(text, num_aug=3)
    print(f"\nOriginal: {text}")
    for i, aug in enumerate(augmented[1:], 1):
        print(f"Aug {i}: {aug}")
```

**Audio:**
```python
# augmentation/audio_aug.py
import torch
import torchaudio
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift

# Audio augmentations
audio_augment = Compose([
    AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
    TimeStretch(min_rate=0.8, max_rate=1.2, p=0.5),
    PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
])

def augment_audio(waveform, sample_rate):
    """Augmentar audio"""
    # Convertir a numpy
    audio_np = waveform.numpy().squeeze()

    # Aplicar augmentations
    augmented = audio_augment(samples=audio_np, sample_rate=sample_rate)

    # Volver a tensor
    return torch.from_numpy(augmented).unsqueeze(0)
```

---

### 3.6 Ensemble Methods ⭐⭐⭐⭐

**Concepto:** Combinar múltiples modelos para mejor performance.

```python
# ensemble/ensemble.py
import torch
import torch.nn as nn
from typing import List
import numpy as np

class ModelEnsemble:
    """Ensemble de múltiples modelos"""

    def __init__(self, models: List[nn.Module], weights: List[float] = None):
        self.models = models
        self.weights = weights if weights else [1.0 / len(models)] * len(models)

        for model in self.models:
            model.eval()

    def predict(self, x, method='weighted_average'):
        """
        Predicción del ensemble

        Methods:
            - weighted_average: Promedio ponderado de probabilidades
            - voting: Voto mayoritario
            - stacking: Usar meta-modelo
        """
        predictions = []

        with torch.no_grad():
            for model in self.models:
                pred = model(x)
                predictions.append(pred)

        if method == 'weighted_average':
            # Promedio ponderado
            ensemble_pred = sum(
                w * pred for w, pred in zip(self.weights, predictions)
            )
            return ensemble_pred

        elif method == 'voting':
            # Voto mayoritario (para clasificación)
            votes = torch.stack([pred.argmax(dim=1) for pred in predictions])
            final_pred = torch.mode(votes, dim=0)[0]
            return final_pred

    def predict_with_uncertainty(self, x):
        """Predicción con estimación de incertidumbre"""
        predictions = []

        with torch.no_grad():
            for model in self.models:
                pred = torch.softmax(model(x), dim=1)
                predictions.append(pred.cpu().numpy())

        predictions = np.array(predictions)

        # Mean prediction
        mean_pred = predictions.mean(axis=0)

        # Uncertainty (std across models)
        uncertainty = predictions.std(axis=0)

        return mean_pred, uncertainty

# Ejemplo: Ensemble de 5 modelos
models = [
    create_model(),
    create_model(),
    create_model(),
    create_model(),
    create_model()
]

# Entrenar cada modelo con seed diferente
for i, model in enumerate(models):
    torch.manual_seed(i)
    train(model, train_loader)

# Crear ensemble
ensemble = ModelEnsemble(models, weights=[0.25, 0.25, 0.2, 0.15, 0.15])

# Predicción
x = torch.randn(1, 3, 224, 224)
pred, uncertainty = ensemble.predict_with_uncertainty(x)

print(f"Prediction: {pred.argmax()}")
print(f"Uncertainty: {uncertainty.max():.4f}")
```

---

## 4. MLOPS PRÁCTICO {#mlops}

### 4.1 Experiment Tracking con MLflow

```python
# mlops/experiment_tracking.py
import mlflow
import mlflow.pytorch
import torch
from typing import Dict

class ExperimentTracker:
    """Wrapper para MLflow experiment tracking"""

    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)
        self.run = None

    def start_run(self, run_name: str = None, tags: Dict = None):
        """Iniciar un run"""
        self.run = mlflow.start_run(run_name=run_name)

        if tags:
            mlflow.set_tags(tags)

        return self.run

    def log_params(self, params: Dict):
        """Log hyperparameters"""
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict, step: int = None):
        """Log metrics"""
        for name, value in metrics.items():
            mlflow.log_metric(name, value, step=step)

    def log_model(self, model, artifact_path: str = "model"):
        """Log PyTorch model"""
        mlflow.pytorch.log_model(model, artifact_path)

    def log_artifact(self, file_path: str):
        """Log archivo (gráfico, config, etc.)"""
        mlflow.log_artifact(file_path)

    def end_run(self):
        """Finalizar run"""
        mlflow.end_run()

# Uso en training loop
def train_with_mlflow(model, train_loader, val_loader, config):
    tracker = ExperimentTracker("my_experiment")

    with tracker.start_run(
        run_name=f"model_{config['architecture']}_lr_{config['learning_rate']}",
        tags={"team": "ml", "project": "classification"}
    ):
        # Log hyperparameters
        tracker.log_params({
            "architecture": config["architecture"],
            "learning_rate": config["learning_rate"],
            "batch_size": config["batch_size"],
            "optimizer": "AdamW"
        })

        # Training loop
        for epoch in range(config["num_epochs"]):
            # Train
            train_loss, train_acc = train_epoch(model, train_loader)

            # Validate
            val_loss, val_acc = validate(model, val_loader)

            # Log metrics
            tracker.log_metrics({
                "train_loss": train_loss,
                "train_accuracy": train_acc,
                "val_loss": val_loss,
                "val_accuracy": val_acc
            }, step=epoch)

            print(f"Epoch {epoch}: Val Acc = {val_acc:.4f}")

        # Log final model
        tracker.log_model(model)

        # Log artifacts (plots, confusion matrix, etc.)
        # save_confusion_matrix("confusion_matrix.png")
        # tracker.log_artifact("confusion_matrix.png")

    return model
```

### 4.2 Model Versioning con DVC

```bash
# Inicializar DVC
dvc init

# Trackear datos
dvc add data/raw/dataset.csv
git add data/raw/dataset.csv.dvc .gitignore

# Trackear modelo
dvc add models/model.pth
git add models/model.pth.dvc

# Configurar remote storage (S3, GCS, Azure, etc.)
dvc remote add -d storage s3://my-bucket/dvc-storage

# Push data/models
dvc push

# Pull data/models (otro developer)
dvc pull
```

**Pipeline DVC:**
```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
      - data/raw/dataset.csv
    outs:
      - data/processed/train.csv
      - data/processed/test.csv

  train:
    cmd: python src/train.py
    deps:
      - data/processed/train.csv
      - src/train.py
    params:
      - train.learning_rate
      - train.batch_size
    outs:
      - models/model.pth
    metrics:
      - metrics/train_metrics.json:
          cache: false

  evaluate:
    cmd: python src/evaluate.py
    deps:
      - models/model.pth
      - data/processed/test.csv
    metrics:
      - metrics/test_metrics.json:
          cache: false
```

```bash
# Ejecutar pipeline completo
dvc repro

# Ver métricas
dvc metrics show

# Comparar experiments
dvc exp show
```

---

### 4.3 Model Monitoring en Producción

```python
# monitoring/model_monitor.py
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from prometheus_client import Counter, Histogram, Gauge
import pandas as pd
import time

# Métricas de Prometheus
prediction_counter = Counter(
    'model_predictions_total',
    'Total predictions made',
    ['model_version', 'endpoint']
)

prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency',
    ['model_version']
)

prediction_confidence = Gauge(
    'model_prediction_confidence',
    'Average prediction confidence',
    ['model_version']
)

data_drift_score = Gauge(
    'model_data_drift_score',
    'Data drift score',
    ['feature']
)

class ModelMonitor:
    """Monitor para modelos en producción"""

    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.predictions_buffer = []
        self.buffer_size = 1000

    def log_prediction(
        self,
        features: dict,
        prediction: float,
        confidence: float,
        model_version: str,
        latency: float
    ):
        """Log una predicción"""

        # Prometheus metrics
        prediction_counter.labels(
            model_version=model_version,
            endpoint='predict'
        ).inc()

        prediction_latency.labels(model_version=model_version).observe(latency)
        prediction_confidence.labels(model_version=model_version).set(confidence)

        # Buffer para drift detection
        self.predictions_buffer.append({
            **features,
            'prediction': prediction,
            'confidence': confidence,
            'timestamp': time.time()
        })

        # Detectar drift cada N predicciones
        if len(self.predictions_buffer) >= self.buffer_size:
            self.detect_drift()

    def detect_drift(self):
        """Detectar data drift"""
        current_data = pd.DataFrame(self.predictions_buffer)

        # Evidently report
        report = Report(metrics=[
            DataDriftPreset(),
        ])

        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=ColumnMapping()
        )

        # Extraer drift scores
        drift_results = report.as_dict()

        # Log drift scores a Prometheus
        for feature, score in drift_results.items():
            data_drift_score.labels(feature=feature).set(score)

        # Alert si drift significativo
        if any(score > 0.3 for score in drift_results.values()):
            self.send_alert("Data drift detected!")

        # Limpiar buffer
        self.predictions_buffer = []

    def send_alert(self, message: str):
        """Enviar alerta (PagerDuty, Slack, etc.)"""
        print(f"ALERT: {message}")
        # Implementar integración con sistema de alertas

# Uso
monitor = ModelMonitor(reference_data=train_data)

@app.post("/predict")
def predict(request: PredictRequest):
    start_time = time.time()

    # Hacer predicción
    prediction = model.predict(request.features)
    confidence = max(prediction)

    latency = time.time() - start_time

    # Log a monitor
    monitor.log_prediction(
        features=request.features,
        prediction=prediction.argmax(),
        confidence=confidence,
        model_version="v1.2.3",
        latency=latency
    )

    return {"prediction": int(prediction.argmax()), "confidence": float(confidence)}
```

---

## 5. DEPLOYMENT PATTERNS {#deployment}

### 5.1 ONNX Export para Inferencia Rápida

```python
# deployment/onnx_export.py
import torch
import onnx
import onnxruntime as ort
import numpy as np

def export_to_onnx(model, dummy_input, onnx_path):
    """Exportar modelo PyTorch a ONNX"""

    model.eval()

    # Export
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )

    # Verificar
    onnx_model = onnx.load(onnx_path)
    onnx.checker.check_model(onnx_model)

    print(f"✓ Model exported to {onnx_path}")

def benchmark_onnx_vs_pytorch(pytorch_model, onnx_path, dummy_input):
    """Comparar velocidad"""
    import time

    # PyTorch inference
    pytorch_model.eval()
    with torch.no_grad():
        start = time.time()
        for _ in range(1000):
            pytorch_model(dummy_input)
        pytorch_time = time.time() - start

    # ONNX inference
    ort_session = ort.InferenceSession(onnx_path)
    input_name = ort_session.get_inputs()[0].name

    dummy_np = dummy_input.cpu().numpy()

    start = time.time()
    for _ in range(1000):
        ort_session.run(None, {input_name: dummy_np})
    onnx_time = time.time() - start

    print(f"\nBenchmark (1000 runs):")
    print(f"PyTorch: {pytorch_time:.3f}s")
    print(f"ONNX: {onnx_time:.3f}s")
    print(f"Speedup: {pytorch_time/onnx_time:.2f}x")

# Uso
model = YourModel()
model.load_state_dict(torch.load('model.pth'))

dummy_input = torch.randn(1, 3, 224, 224)

export_to_onnx(model, dummy_input, 'model.onnx')
benchmark_onnx_vs_pytorch(model, 'model.onnx', dummy_input)
```

### 5.2 FastAPI Serving

```python
# deployment/serve.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np
from PIL import Image
import io
from prometheus_client import make_asgi_app, Counter, Histogram
import time

app = FastAPI(title="ML Model API")

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

# Cargar modelo ONNX
ort_session = ort.InferenceSession('model.onnx')
input_name = ort_session.get_inputs()[0].name

class PredictionResponse(BaseModel):
    prediction: int
    confidence: float
    latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """Endpoint de predicción"""

    start_time = time.time()

    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()

    try:
        # Leer imagen
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')

        # Preprocessing
        image = image.resize((224, 224))
        image_array = np.array(image).astype(np.float32) / 255.0
        image_array = np.transpose(image_array, (2, 0, 1))  # HWC -> CHW
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dim

        # Inferencia
        outputs = ort_session.run(None, {input_name: image_array})
        prediction = outputs[0][0]

        # Post-processing
        predicted_class = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        latency = (time.time() - start_time) * 1000  # ms

        REQUEST_LATENCY.observe(latency / 1000)

        return PredictionResponse(
            prediction=predicted_class,
            confidence=confidence,
            latency_ms=latency
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}

# Métricas de Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and code
COPY model.onnx .
COPY serve.py .

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: model
        image: ml-model:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model
spec:
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 6. ROADMAP DE APRENDIZAJE {#roadmap}

### Nivel 1: Fundamentos (2-4 semanas)

**Semana 1-2: Python + NumPy + Pandas**
- [ ] Manipulación de arrays con NumPy
- [ ] Limpieza de datos con Pandas
- [ ] Visualización con Matplotlib/Seaborn
- [ ] Proyecto: Análisis exploratorio de dataset

**Semana 3-4: ML Básico con Scikit-Learn**
- [ ] Regresión lineal/logística
- [ ] Árboles de decisión, Random Forest
- [ ] Métricas: accuracy, precision, recall, F1
- [ ] Train/test split, cross-validation
- [ ] Proyecto: Clasificador de iris o titanic

### Nivel 2: Deep Learning (4-6 semanas)

**Semana 5-7: PyTorch Básico**
- [ ] Tensores y operaciones
- [ ] Autograd y backpropagation
- [ ] Redes neuronales simples
- [ ] Training loops
- [ ] Proyecto: MNIST classifier

**Semana 8-10: CNNs y Transfer Learning**
- [ ] Convolutional layers
- [ ] Arquitecturas: ResNet, EfficientNet
- [ ] Transfer learning
- [ ] Data augmentation
- [ ] Proyecto: Image classifier custom

### Nivel 3: Producción (4-8 semanas)

**Semana 11-14: MLOps**
- [ ] Experiment tracking (MLflow/W&B)
- [ ] Model versioning (DVC)
- [ ] ONNX export
- [ ] FastAPI serving
- [ ] Proyecto: Deploy modelo en Kubernetes

**Semana 15-18: Advanced Topics**
- [ ] Model monitoring y drift detection
- [ ] A/B testing de modelos
- [ ] Feature stores
- [ ] CI/CD para ML
- [ ] Proyecto: Sistema ML completo en producción

---

## 📚 Recursos Recomendados

**Cursos:**
- Fast.ai Practical Deep Learning
- Andrew Ng's Machine Learning Specialization
- Full Stack Deep Learning

**Libros:**
- "Designing Machine Learning Systems" - Chip Huyen
- "Machine Learning Engineering" - Andriy Burkov
- "Deep Learning with PyTorch" - Stevens et al.

**Comunidades:**
- r/MachineLearning
- Papers With Code
- Hugging Face Forums

---

**Versión:** 1.0
**Última actualización:** 2024-12-03
**Próxima revisión:** 2025-03-01
**Mantenedor:** Equipo ML Engineering
