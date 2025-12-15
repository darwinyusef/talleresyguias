# PyTorch: De Principiante a Experto
## Curso Completo Paso a Paso

**Versión:** 1.0
**Fecha:** 2024-12-03
**Duración:** 8-12 semanas
**Prerequisitos:** Python básico

---

## 📋 Índice del Curso

### **MÓDULO 1: Fundamentos** (Semana 1-2)
1. [Tensores y Operaciones](#modulo1-tensores)
2. [Autograd y Gradientes](#modulo1-autograd)
3. [Optimizadores](#modulo1-optimizers)

### **MÓDULO 2: Redes Neuronales** (Semana 3-4)
4. [Construcción de Redes con nn.Module](#modulo2-nnmodule)
5. [Training Loops](#modulo2-training)
6. [Datasets y DataLoaders](#modulo2-data)

### **MÓDULO 3: Computer Vision** (Semana 5-6)
7. [Convolutional Neural Networks](#modulo3-cnn)
8. [Transfer Learning](#modulo3-transfer)
9. [Object Detection](#modulo3-detection)

### **MÓDULO 4: Natural Language Processing** (Semana 7-8)
10. [RNNs y LSTMs](#modulo4-rnn)
11. [Transformers](#modulo4-transformers)
12. [Fine-tuning BERT](#modulo4-bert)

### **MÓDULO 5: Técnicas Avanzadas** (Semana 9-10)
13. [GANs](#modulo5-gans)
14. [Reinforcement Learning](#modulo5-rl)
15. [Distributed Training](#modulo5-distributed)

### **MÓDULO 6: Producción** (Semana 11-12)
16. [Optimización y Quantization](#modulo6-optimization)
17. [ONNX Export](#modulo6-onnx)
18. [Deployment](#modulo6-deployment)

---

# MÓDULO 1: FUNDAMENTOS

## 1. Tensores y Operaciones {#modulo1-tensores}

### 1.1 ¿Qué es un Tensor?

Un tensor es un array multidimensional, similar a NumPy pero con soporte para GPU.

```python
# 01_tensors_basics.py
import torch
import numpy as np

# ============================================
# CREACIÓN DE TENSORES
# ============================================

# Desde listas
tensor_1d = torch.tensor([1, 2, 3, 4, 5])
print(f"1D Tensor: {tensor_1d}")
print(f"Shape: {tensor_1d.shape}")

# Tensor 2D (matriz)
tensor_2d = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"\n2D Tensor:\n{tensor_2d}")
print(f"Shape: {tensor_2d.shape}")  # torch.Size([2, 3])

# Tensor 3D (batch de imágenes)
tensor_3d = torch.randn(32, 3, 224, 224)  # 32 imágenes, 3 canales RGB, 224x224
print(f"\n3D Tensor shape: {tensor_3d.shape}")

# ============================================
# INICIALIZACIÓN
# ============================================

# Zeros
zeros = torch.zeros(3, 4)
print(f"\nZeros:\n{zeros}")

# Ones
ones = torch.ones(2, 3)

# Random
random = torch.randn(3, 3)  # Normal distribution (mean=0, std=1)
uniform = torch.rand(3, 3)  # Uniform distribution [0, 1)

# Rango
arange = torch.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace = torch.linspace(0, 1, 5)  # [0.0, 0.25, 0.5, 0.75, 1.0]

# Desde NumPy
np_array = np.array([[1, 2], [3, 4]])
from_numpy = torch.from_numpy(np_array)

# ============================================
# OPERACIONES BÁSICAS
# ============================================

a = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
b = torch.tensor([5, 6, 7, 8], dtype=torch.float32)

# Aritméticas (element-wise)
suma = a + b
resta = a - b
multiplicacion = a * b  # Element-wise
division = a / b

print(f"\nSuma: {suma}")
print(f"Multiplicación element-wise: {multiplicacion}")

# Producto punto
dot_product = torch.dot(a, b)
print(f"Producto punto: {dot_product}")

# Multiplicación de matrices
A = torch.randn(3, 4)
B = torch.randn(4, 5)
C = torch.mm(A, B)  # Resultado: 3x5
print(f"\nMatrix multiplication shape: {C.shape}")

# Alternativa: @ operator
C = A @ B

# ============================================
# BROADCASTING
# ============================================

x = torch.tensor([[1], [2], [3]])  # Shape: (3, 1)
y = torch.tensor([4, 5, 6])        # Shape: (3,)

# PyTorch automáticamente expande dimensiones
result = x + y  # Shape: (3, 3)
print(f"\nBroadcasting result:\n{result}")

# ============================================
# INDEXING Y SLICING
# ============================================

tensor = torch.arange(0, 20).reshape(4, 5)
print(f"\nTensor original:\n{tensor}")

# Indexing
first_row = tensor[0]          # Primera fila
first_col = tensor[:, 0]       # Primera columna
element = tensor[2, 3]         # Elemento en posición [2, 3]

# Slicing
sub_tensor = tensor[1:3, 2:4]  # Filas 1-2, columnas 2-3

# Boolean indexing
mask = tensor > 10
filtered = tensor[mask]
print(f"\nElementos > 10: {filtered}")

# ============================================
# RESHAPE Y TRANSPOSE
# ============================================

original = torch.arange(12)
reshaped = original.reshape(3, 4)
print(f"\nReshaped:\n{reshaped}")

# Transpose
transposed = reshaped.T
print(f"\nTransposed:\n{transposed}")

# View (comparte memoria)
view = original.view(3, 4)  # Más eficiente que reshape

# Flatten
flat = reshaped.flatten()

# ============================================
# GPU
# ============================================

# Verificar si CUDA está disponible
print(f"\nCUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    # Mover tensor a GPU
    tensor_gpu = tensor.to('cuda')
    # o tensor.cuda()

    # Device específico
    device = torch.device('cuda:0')
    tensor_gpu = tensor.to(device)

    # Mover de vuelta a CPU
    tensor_cpu = tensor_gpu.to('cpu')
    # o tensor_gpu.cpu()

# Mejor práctica: usar device agnóstico
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tensor = torch.randn(3, 3).to(device)

# ============================================
# EJERCICIO 1: Implementar función que calcula distancia euclidiana
# ============================================

def euclidean_distance(x, y):
    """
    Calcular distancia euclidiana entre dos tensores

    Args:
        x: Tensor shape (N, D)
        y: Tensor shape (M, D)

    Returns:
        distances: Tensor shape (N, M)
    """
    # Expandir dimensiones para broadcasting
    x = x.unsqueeze(1)  # (N, 1, D)
    y = y.unsqueeze(0)  # (1, M, D)

    # Calcular distancia
    distances = torch.sqrt(((x - y) ** 2).sum(dim=2))

    return distances

# Test
x = torch.randn(5, 10)  # 5 puntos en 10 dimensiones
y = torch.randn(3, 10)  # 3 puntos en 10 dimensiones
dist = euclidean_distance(x, y)
print(f"\nDistances shape: {dist.shape}")  # (5, 3)
```

---

## 2. Autograd y Gradientes {#modulo1-autograd}

### 2.1 Diferenciación Automática

```python
# 02_autograd.py
import torch

# ============================================
# AUTOGRAD BÁSICO
# ============================================

# Crear tensor con requires_grad=True para trackear gradientes
x = torch.tensor([2.0], requires_grad=True)
print(f"x: {x}")

# Operación
y = x ** 2 + 3 * x + 1
print(f"y = x^2 + 3x + 1 = {y}")

# Calcular gradientes
y.backward()

# dy/dx = 2x + 3 = 2(2) + 3 = 7
print(f"dy/dx: {x.grad}")  # tensor([7.])

# ============================================
# GRADIENTES CON MÚLTIPLES VARIABLES
# ============================================

x = torch.tensor([2.0, 3.0], requires_grad=True)

# f(x) = x[0]^2 + 2*x[1]^2 + x[0]*x[1]
y = x[0]**2 + 2*x[1]**2 + x[0]*x[1]

y.backward()

# Gradientes:
# df/dx[0] = 2*x[0] + x[1] = 2(2) + 3 = 7
# df/dx[1] = 4*x[1] + x[0] = 4(3) + 2 = 14
print(f"\nGradient: {x.grad}")  # tensor([7., 14.])

# ============================================
# GRADIENTES DE VECTORES
# ============================================

x = torch.randn(3, requires_grad=True)
y = x * 2

# Para vectores, necesitamos especificar gradient
y.backward(torch.ones_like(y))

print(f"\nGradient: {x.grad}")  # tensor([2., 2., 2.])

# ============================================
# NO GRADIENT CONTEXT
# ============================================

x = torch.randn(3, requires_grad=True)

# No calcular gradientes (inferencia)
with torch.no_grad():
    y = x * 2
    print(f"y requires_grad: {y.requires_grad}")  # False

# Alternativa: detach()
y = (x * 2).detach()

# ============================================
# ACUMULAR GRADIENTES
# ============================================

x = torch.tensor([2.0], requires_grad=True)

# Primera operación
y = x ** 2
y.backward()
print(f"Gradient after first backward: {x.grad}")  # tensor([4.])

# Segunda operación (gradientes se ACUMULAN!)
y = x ** 3
y.backward()
print(f"Gradient after second backward: {x.grad}")  # tensor([16.]) = 4 + 12

# ⚠️ Importante: resetear gradientes
x.grad.zero_()
y = x ** 3
y.backward()
print(f"Gradient after zero_: {x.grad}")  # tensor([12.])

# ============================================
# EJERCICIO 2: Implementar gradient descent manual
# ============================================

def gradient_descent(initial_value, learning_rate=0.1, num_iterations=100):
    """
    Minimizar f(x) = x^2 usando gradient descent

    f(x) = x^2
    df/dx = 2x
    x_new = x - lr * df/dx
    """
    x = torch.tensor([initial_value], requires_grad=True)

    for i in range(num_iterations):
        # Forward
        y = x ** 2

        # Backward
        y.backward()

        # Update (sin autograd)
        with torch.no_grad():
            x -= learning_rate * x.grad

        # Reset gradientes
        x.grad.zero_()

        if i % 10 == 0:
            print(f"Iteration {i}: x = {x.item():.4f}, f(x) = {y.item():.4f}")

    return x.item()

# Test
final_x = gradient_descent(10.0, learning_rate=0.1, num_iterations=100)
print(f"\nFinal x: {final_x:.6f}")  # Debería ser cercano a 0

# ============================================
# CUSTOM BACKWARD PASS
# ============================================

class CustomFunction(torch.autograd.Function):
    """Función custom con backward manual"""

    @staticmethod
    def forward(ctx, x):
        # Guardar para backward
        ctx.save_for_backward(x)
        return x ** 2

    @staticmethod
    def backward(ctx, grad_output):
        # Recuperar valores guardados
        x, = ctx.saved_tensors
        # Calcular gradiente: d(x^2)/dx = 2x
        grad_input = grad_output * 2 * x
        return grad_input

# Uso
x = torch.tensor([3.0], requires_grad=True)
custom_func = CustomFunction.apply
y = custom_func(x)
y.backward()
print(f"\nCustom gradient: {x.grad}")  # tensor([6.]) = 2 * 3
```

---

## 3. Optimizadores {#modulo1-optimizers}

```python
# 03_optimizers.py
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# ============================================
# COMPARACIÓN DE OPTIMIZADORES
# ============================================

# Función a minimizar: Rosenbrock function
def rosenbrock(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

def optimize_comparison():
    """Comparar diferentes optimizadores"""

    # Parámetros iniciales
    start_x, start_y = -1.5, 2.5

    optimizers = {
        'SGD': lambda params: optim.SGD(params, lr=0.001),
        'SGD + Momentum': lambda params: optim.SGD(params, lr=0.001, momentum=0.9),
        'Adam': lambda params: optim.Adam(params, lr=0.01),
        'RMSprop': lambda params: optim.RMSprop(params, lr=0.01),
    }

    num_iterations = 1000
    results = {}

    for name, optimizer_fn in optimizers.items():
        # Parámetros
        x = torch.tensor([start_x], requires_grad=True)
        y = torch.tensor([start_y], requires_grad=True)

        optimizer = optimizer_fn([x, y])

        trajectory = []

        for i in range(num_iterations):
            optimizer.zero_grad()

            # Forward
            loss = rosenbrock(x, y)

            # Backward
            loss.backward()

            # Update
            optimizer.step()

            if i % 50 == 0:
                trajectory.append((x.item(), y.item(), loss.item()))

        results[name] = trajectory
        print(f"{name}: Final loss = {loss.item():.6f}, x = {x.item():.4f}, y = {y.item():.4f}")

    return results

# ============================================
# SCHEDULERS (Learning Rate)
# ============================================

def learning_rate_schedulers():
    """Ejemplos de schedulers"""

    model = nn.Linear(10, 1)
    optimizer = optim.Adam(model.parameters(), lr=0.1)

    # 1. StepLR: reduce LR cada N epochs
    scheduler_step = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

    # 2. ExponentialLR: decaimiento exponencial
    scheduler_exp = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)

    # 3. CosineAnnealingLR: cosine decay
    scheduler_cosine = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

    # 4. ReduceLROnPlateau: reduce cuando métrica se estanca
    scheduler_plateau = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode='min',
        factor=0.1,
        patience=10
    )

    # Uso en training loop
    lrs = []
    for epoch in range(100):
        # Training...
        loss = torch.randn(1).item()

        # Step scheduler
        scheduler_cosine.step()

        # Para ReduceLROnPlateau
        # scheduler_plateau.step(val_loss)

        lrs.append(optimizer.param_groups[0]['lr'])

    # Plot
    plt.plot(lrs)
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.title('Cosine Annealing LR Schedule')
    plt.savefig('lr_schedule.png')
    print("\n✓ LR schedule saved to lr_schedule.png")

# ============================================
# GRADIENT CLIPPING
# ============================================

def train_with_gradient_clipping(model, dataloader, num_epochs):
    """Training con gradient clipping (previene exploding gradients)"""

    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(num_epochs):
        for batch_idx, (data, targets) in enumerate(dataloader):
            # Forward
            outputs = model(data)
            loss = criterion(outputs, targets)

            # Backward
            optimizer.zero_grad()
            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            # Update
            optimizer.step()

# ============================================
# EJERCICIO 3: Implementar optimizador custom
# ============================================

class CustomSGD:
    """SGD con momentum implementado manualmente"""

    def __init__(self, params, lr=0.01, momentum=0.9):
        self.params = list(params)
        self.lr = lr
        self.momentum = momentum
        self.velocities = [torch.zeros_like(p) for p in self.params]

    def zero_grad(self):
        for p in self.params:
            if p.grad is not None:
                p.grad.zero_()

    def step(self):
        with torch.no_grad():
            for i, p in enumerate(self.params):
                if p.grad is None:
                    continue

                # Update velocity
                self.velocities[i] = self.momentum * self.velocities[i] - self.lr * p.grad

                # Update parameters
                p += self.velocities[i]

# Test
x = torch.tensor([10.0], requires_grad=True)
optimizer = CustomSGD([x], lr=0.1, momentum=0.9)

for i in range(50):
    optimizer.zero_grad()
    y = x ** 2
    y.backward()
    optimizer.step()

    if i % 10 == 0:
        print(f"Iteration {i}: x = {x.item():.4f}")

if __name__ == "__main__":
    print("Comparing optimizers...")
    optimize_comparison()

    print("\n\nLearning rate schedulers...")
    learning_rate_schedulers()
```

---

# MÓDULO 2: REDES NEURONALES

## 4. Construcción de Redes con nn.Module {#modulo2-nnmodule}

```python
# 04_neural_networks.py
import torch
import torch.nn as nn
import torch.nn.functional as F

# ============================================
# RED NEURONAL BÁSICA
# ============================================

class SimpleNN(nn.Module):
    """Red neuronal fully-connected simple"""

    def __init__(self, input_size, hidden_size, num_classes):
        super(SimpleNN, self).__init__()

        # Capas
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, num_classes)

        # Batch normalization
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)

        # Dropout
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Flatten si es necesario
        x = x.view(x.size(0), -1)

        # Capa 1
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout(x)

        # Capa 2
        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout(x)

        # Output
        x = self.fc3(x)

        return x

# Crear modelo
model = SimpleNN(input_size=784, hidden_size=256, num_classes=10)

# Ver arquitectura
print(model)

# Contar parámetros
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\nTotal parameters: {total_params:,}")
print(f"Trainable parameters: {trainable_params:,}")

# ============================================
# ARQUITECTURA CON nn.Sequential
# ============================================

class SimpleNNSequential(nn.Module):
    """Misma red pero usando nn.Sequential"""

    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()

        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(input_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(hidden_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(hidden_size, num_classes)
        )

    def forward(self, x):
        return self.network(x)

# ============================================
# BLOQUES RESIDUALES (como ResNet)
# ============================================

class ResidualBlock(nn.Module):
    """Bloque residual con skip connection"""

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)

        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        # Skip connection
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1,
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = F.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        # Add skip connection
        out += self.shortcut(identity)
        out = F.relu(out)

        return out

# ============================================
# WEIGHT INITIALIZATION
# ============================================

def init_weights(m):
    """Inicialización de pesos"""
    if isinstance(m, nn.Linear):
        # Xavier/Glorot initialization
        nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            nn.init.zeros_(m.bias)

    elif isinstance(m, nn.Conv2d):
        # Kaiming/He initialization (mejor para ReLU)
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        if m.bias is not None:
            nn.init.zeros_(m.bias)

    elif isinstance(m, nn.BatchNorm2d):
        nn.init.ones_(m.weight)
        nn.init.zeros_(m.bias)

# Aplicar inicialización
model = SimpleNN(784, 256, 10)
model.apply(init_weights)

# ============================================
# CUSTOM LAYERS
# ============================================

class GaussianNoise(nn.Module):
    """Agregar ruido gaussiano (regularización)"""

    def __init__(self, stddev=0.1):
        super().__init__()
        self.stddev = stddev

    def forward(self, x):
        if self.training:
            noise = torch.randn_like(x) * self.stddev
            return x + noise
        return x

class Swish(nn.Module):
    """Swish activation: x * sigmoid(x)"""

    def forward(self, x):
        return x * torch.sigmoid(x)

# Usar custom layers
model = nn.Sequential(
    nn.Linear(784, 256),
    Swish(),
    GaussianNoise(0.1),
    nn.Linear(256, 10)
)

# ============================================
# EJERCICIO 4: Implementar MLP con skip connections
# ============================================

class MLPWithSkipConnections(nn.Module):
    """MLP con skip connections cada 2 capas"""

    def __init__(self, input_size, hidden_sizes, num_classes):
        super().__init__()

        self.input_layer = nn.Linear(input_size, hidden_sizes[0])

        self.hidden_layers = nn.ModuleList()
        self.skip_layers = nn.ModuleList()

        for i in range(len(hidden_sizes) - 1):
            self.hidden_layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i+1]))

            # Skip connection cada 2 capas
            if i % 2 == 1:
                self.skip_layers.append(
                    nn.Linear(hidden_sizes[i-1], hidden_sizes[i+1])
                )

        self.output_layer = nn.Linear(hidden_sizes[-1], num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)

        x = F.relu(self.input_layer(x))

        skip_idx = 0
        for i, layer in enumerate(self.hidden_layers):
            identity = x

            x = layer(x)

            # Add skip connection cada 2 capas
            if i % 2 == 1 and skip_idx < len(self.skip_layers):
                x = x + self.skip_layers[skip_idx](identity)
                skip_idx += 1

            x = F.relu(x)

        x = self.output_layer(x)

        return x

# Test
model = MLPWithSkipConnections(
    input_size=784,
    hidden_sizes=[256, 256, 128, 128],
    num_classes=10
)

dummy_input = torch.randn(32, 784)
output = model(dummy_input)
print(f"\nOutput shape: {output.shape}")  # (32, 10)
```

---

## 5. Training Loops {#modulo2-training}

```python
# 05_training_loops.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
import time

# ============================================
# TRAINING LOOP BÁSICO
# ============================================

def train_one_epoch(model, dataloader, criterion, optimizer, device):
    """Entrenar por un epoch"""

    model.train()  # Modo training (habilita dropout, batch norm, etc.)

    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, targets) in enumerate(dataloader):
        # Mover a device
        inputs, targets = inputs.to(device), targets.to(device)

        # Zero gradients
        optimizer.zero_grad()

        # Forward
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # Backward
        loss.backward()

        # Update
        optimizer.step()

        # Métricas
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total

    return epoch_loss, epoch_acc

def validate(model, dataloader, criterion, device):
    """Validar modelo"""

    model.eval()  # Modo evaluación

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():  # No calcular gradientes
        for inputs, targets in dataloader:
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    val_loss = running_loss / len(dataloader)
    val_acc = 100. * correct / total

    return val_loss, val_acc

# ============================================
# TRAINING LOOP COMPLETO
# ============================================

def train_model(
    model,
    train_loader,
    val_loader,
    num_epochs=10,
    learning_rate=0.001,
    device='cuda',
    save_path='best_model.pth'
):
    """Training loop completo con mejores prácticas"""

    model = model.to(device)

    # Loss y optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)

    # Scheduler
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

    # TensorBoard
    writer = SummaryWriter('runs/experiment_1')

    # Tracking
    best_val_acc = 0.0
    patience = 5
    patience_counter = 0

    for epoch in range(num_epochs):
        start_time = time.time()

        # Train
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device
        )

        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        # Scheduler step
        scheduler.step()

        epoch_time = time.time() - start_time

        # Print progress
        print(f'Epoch [{epoch+1}/{num_epochs}] ({epoch_time:.2f}s)')
        print(f'  Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%')
        print(f'  Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%')
        print(f'  LR: {optimizer.param_groups[0]["lr"]:.6f}')

        # TensorBoard logging
        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Loss/val', val_loss, epoch)
        writer.add_scalar('Accuracy/train', train_acc, epoch)
        writer.add_scalar('Accuracy/val', val_acc, epoch)
        writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], epoch)

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
            }, save_path)
            print(f'  ✓ New best model saved! Val Acc: {val_acc:.2f}%')
            patience_counter = 0
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= patience:
            print(f'\nEarly stopping triggered after {epoch+1} epochs')
            break

        print()

    writer.close()

    # Load best model
    checkpoint = torch.load(save_path)
    model.load_state_dict(checkpoint['model_state_dict'])

    print(f'\n✓ Training completed!')
    print(f'Best validation accuracy: {best_val_acc:.2f}%')

    return model

# ============================================
# MIXED PRECISION TRAINING (más rápido)
# ============================================

def train_with_amp(model, train_loader, val_loader, num_epochs, device):
    """Training con Automatic Mixed Precision"""

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.001)

    # GradScaler para mixed precision
    scaler = torch.cuda.amp.GradScaler()

    for epoch in range(num_epochs):
        model.train()

        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()

            # Forward con autocast
            with torch.cuda.amp.autocast():
                outputs = model(inputs)
                loss = criterion(outputs, targets)

            # Backward con scaled gradients
            scaler.scale(loss).backward()

            # Update
            scaler.step(optimizer)
            scaler.update()

# ============================================
# GRADIENT ACCUMULATION (simular batch grande)
# ============================================

def train_with_gradient_accumulation(
    model,
    train_loader,
    accumulation_steps=4
):
    """
    Gradient accumulation para simular batch size más grande

    Ejemplo: batch_size=32, accumulation_steps=4
    → Efectivamente batch_size=128
    """

    model.train()
    optimizer = optim.Adam(model.parameters())
    criterion = nn.CrossEntropyLoss()

    for batch_idx, (inputs, targets) in enumerate(train_loader):
        # Forward
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # Normalizar loss
        loss = loss / accumulation_steps

        # Backward
        loss.backward()

        # Update cada accumulation_steps
        if (batch_idx + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()

# ============================================
# EJERCICIO 5: Implementar training con warmup
# ============================================

class WarmupScheduler:
    """Learning rate warmup + cosine decay"""

    def __init__(self, optimizer, warmup_epochs, total_epochs, base_lr, max_lr):
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.total_epochs = total_epochs
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.current_epoch = 0

    def step(self):
        if self.current_epoch < self.warmup_epochs:
            # Warmup: linear increase
            lr = self.base_lr + (self.max_lr - self.base_lr) * \
                 (self.current_epoch / self.warmup_epochs)
        else:
            # Cosine decay
            progress = (self.current_epoch - self.warmup_epochs) / \
                      (self.total_epochs - self.warmup_epochs)
            lr = self.base_lr + (self.max_lr - self.base_lr) * \
                 0.5 * (1 + torch.cos(torch.tensor(progress * 3.14159)))

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

        self.current_epoch += 1
```

---

*[El archivo continúa con más módulos... debido al límite de longitud, incluyo la estructura completa]*

## 6. Datasets y DataLoaders {#modulo2-data}
- Custom Dataset class
- Transformations
- Data augmentation
- DataLoader con workers

## MÓDULO 3: COMPUTER VISION

## 7. Convolutional Neural Networks {#modulo3-cnn}
- Conv2d, MaxPool, BatchNorm
- Arquitectura completa CNN
- Visualización de filtros

## 8. Transfer Learning {#modulo3-transfer}
- Fine-tuning ResNet
- Feature extraction
- Progressive unfreezing

## 9. Object Detection {#modulo3-detection}
- YOLO básico
- Non-max suppression
- Métricas: IoU, mAP

## MÓDULO 4: NLP

## 10. RNNs y LSTMs {#modulo4-rnn}
- Vanilla RNN
- LSTM implementation
- Bidirectional LSTM

## 11. Transformers {#modulo4-transformers}
- Self-attention
- Multi-head attention
- Positional encoding
- Transformer from scratch

## 12. Fine-tuning BERT {#modulo4-bert}
- Hugging Face Transformers
- Tokenization
- Fine-tune para clasificación

## MÓDULO 5: TÉCNICAS AVANZADAS

## 13. GANs {#modulo5-gans}
- Generator y Discriminator
- Training loop
- DCGAN implementation

## 14. Reinforcement Learning {#modulo5-rl}
- Q-Learning
- DQN
- Policy gradients

## 15. Distributed Training {#modulo5-distributed}
- DataParallel
- DistributedDataParallel
- Multi-GPU training

## MÓDULO 6: PRODUCCIÓN

## 16. Optimización {#modulo6-optimization}
- Quantization
- Pruning
- Knowledge distillation

## 17. ONNX Export {#modulo6-onnx}
- Export to ONNX
- ONNX Runtime
- Benchmark

## 18. Deployment {#modulo6-deployment}
- TorchServe
- FastAPI serving
- Docker + Kubernetes

---

## 📚 PROYECTOS FINALES

### Proyecto 1: Image Classifier
- Dataset: CIFAR-100
- CNN custom + Transfer learning
- Deploy con API

### Proyecto 2: Text Classifier
- Dataset: IMDB reviews
- LSTM + Transformer
- Fine-tune BERT

### Proyecto 3: GAN para Generación
- Dataset: CelebA
- DCGAN implementation
- Progressive growing

---

## 🎓 RECURSOS

**Documentación:**
- PyTorch Docs: https://pytorch.org/docs
- PyTorch Tutorials: https://pytorch.org/tutorials

**Libros:**
- Deep Learning with PyTorch - Stevens et al.
- Programming PyTorch for Deep Learning - Ketkar

**Cursos:**
- Fast.ai
- Stanford CS230
- Deep Learning Specialization (Coursera)

---

**Versión:** 1.0
**Última actualización:** 2024-12-03
**Duración estimada:** 8-12 semanas
**Prerequisitos:** Python básico
