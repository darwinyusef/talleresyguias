# 🔄 State Management - Gestión de Estado

> **Jetpack Compose (Android) & SwiftUI (iOS) - Manejo de Estado y Reactividad**

---

## 🎯 Objetivo

Dominar la gestión de estado en aplicaciones declarativas: estado local, estado compartido, y arquitectura MVVM.

---

## 📚 Conceptos Fundamentales

### ¿Qué es el Estado?

El **estado** es cualquier valor que puede cambiar con el tiempo y que determina cómo se ve la UI.

```
Estado → UI
```

Si el estado cambia, la UI se actualiza automáticamente.

### Tipos de Estado

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Local** | Solo una pantalla lo necesita | Toggle de switch, texto de input |
| **Compartido** | Múltiples pantallas lo necesitan | Usuario logueado, carrito de compras |
| **Persistente** | Sobrevive al cerrar la app | Configuración, favoritos |

---

## 🔧 Estado Local

### Jetpack Compose - remember & mutableStateOf

#### Estado Simple

```kotlin
@Composable
fun CounterExample() {
    // Estado que se recuerda entre recomposiciones
    var count by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Contador: $count",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { count-- }) {
                Text("-")
            }

            Button(onClick = { count++ }) {
                Text("+")
            }

            Button(onClick = { count = 0 }) {
                Text("Reset")
            }
        }
    }
}
```

#### Estado de Múltiples Valores

```kotlin
@Composable
fun FormExample() {
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var isSubscribed by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Nombre") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        Row(
            verticalAlignment = Alignment.CenterVertically
        ) {
            Checkbox(
                checked = isSubscribed,
                onCheckedChange = { isSubscribed = it }
            )
            Text("Suscribirse al newsletter")
        }

        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = { /* Submit */ },
            modifier = Modifier.fillMaxWidth(),
            enabled = name.isNotBlank() && email.isNotBlank()
        ) {
            Text("Enviar")
        }

        // Mostrar valores
        if (name.isNotBlank()) {
            Spacer(modifier = Modifier.height(16.dp))
            Text("Hola, $name!")
            if (isSubscribed) {
                Text("Te enviaremos emails a: $email", fontSize = 12.sp, color = Color.Gray)
            }
        }
    }
}
```

#### Estado de Objetos

```kotlin
data class User(
    val name: String = "",
    val email: String = "",
    val age: Int = 0
)

@Composable
fun UserFormExample() {
    var user by remember { mutableStateOf(User()) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        OutlinedTextField(
            value = user.name,
            onValueChange = { user = user.copy(name = it) },
            label = { Text("Nombre") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = user.email,
            onValueChange = { user = user.copy(email = it) },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = if (user.age == 0) "" else user.age.toString(),
            onValueChange = { user = user.copy(age = it.toIntOrNull() ?: 0) },
            label = { Text("Edad") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "Usuario: ${user.name}, ${user.age} años",
            style = MaterialTheme.typography.bodyLarge
        )
    }
}
```

#### rememberSaveable - Sobrevive a cambios de configuración

```kotlin
@Composable
fun CounterWithSaveable() {
    // Sobrevive a rotaciones de pantalla
    var count by rememberSaveable { mutableStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Contador (sobrevive rotación): $count")
        Button(onClick = { count++ }) {
            Text("Incrementar")
        }
    }
}
```

---

### SwiftUI - @State

#### Estado Simple

```swift
struct CounterExample: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 16) {
            Text("Contador: \(count)")
                .font(.largeTitle)

            HStack(spacing: 8) {
                Button("-") {
                    count -= 1
                }

                Button("+") {
                    count += 1
                }

                Button("Reset") {
                    count = 0
                }
            }
            .buttonStyle(.bordered)
        }
    }
}
```

#### Estado de Múltiples Valores

```swift
struct FormExample: View {
    @State private var name = ""
    @State private var email = ""
    @State private var isSubscribed = false

    var body: some View {
        Form {
            Section {
                TextField("Nombre", text: $name)
                TextField("Email", text: $email)
                    .keyboardType(.emailAddress)
                    .textInputAutocapitalization(.never)
            }

            Section {
                Toggle("Suscribirse al newsletter", isOn: $isSubscribed)
            }

            Section {
                Button("Enviar") {
                    // Submit
                }
                .disabled(name.isEmpty || email.isEmpty)
            }

            if !name.isEmpty {
                Section {
                    Text("Hola, \(name)!")
                    if isSubscribed {
                        Text("Te enviaremos emails a: \(email)")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                }
            }
        }
    }
}
```

#### Estado de Objetos

```swift
struct User {
    var name: String = ""
    var email: String = ""
    var age: Int = 0
}

struct UserFormExample: View {
    @State private var user = User()

    var body: some View {
        Form {
            TextField("Nombre", text: $user.name)

            TextField("Email", text: $user.email)
                .keyboardType(.emailAddress)
                .textInputAutocapitalization(.never)

            TextField("Edad", value: $user.age, format: .number)
                .keyboardType(.numberPad)

            Section {
                Text("Usuario: \(user.name), \(user.age) años")
            }
        }
    }
}
```

---

### Comparación Estado Local

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Declarar estado | `var x by remember { mutableStateOf(0) }` | `@State private var x = 0` |
| Modificar | `x = 10` | `x = 10` |
| Binding | Pasar callback | Pasar `$x` |
| Sobrevive rotación | `rememberSaveable` | Automático |

---

## 🔗 Compartir Estado - State Hoisting

### Jetpack Compose

#### Problema: Estado Duplicado

```kotlin
// ❌ Mal: Cada componente tiene su propio estado
@Composable
fun BadExample() {
    Column {
        CounterDisplay()  // Tiene su propio count
        CounterDisplay()  // Tiene su propio count diferente
    }
}
```

#### Solución: Elevar el Estado (State Hoisting)

```kotlin
// ✅ Bien: Estado compartido
@Composable
fun GoodExample() {
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Contador compartido: $count")
        CounterButton(
            count = count,
            onIncrement = { count++ }
        )
        CounterButton(
            count = count,
            onIncrement = { count++ }
        )
    }
}

@Composable
fun CounterButton(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Incrementar (actual: $count)")
    }
}
```

#### Ejemplo Completo: Todo List

```kotlin
data class Todo(
    val id: Int,
    val text: String,
    val completed: Boolean = false
)

@Composable
fun TodoApp() {
    var todos by remember {
        mutableStateOf(
            listOf(
                Todo(1, "Aprender Compose"),
                Todo(2, "Practicar layouts"),
                Todo(3, "Crear una app")
            )
        )
    }
    var newTodoText by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize()) {
        // Header
        Text(
            text = "Mis Tareas",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(16.dp)
        )

        // Add todo
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = newTodoText,
                onValueChange = { newTodoText = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("Nueva tarea") }
            )

            Spacer(modifier = Modifier.width(8.dp))

            Button(
                onClick = {
                    if (newTodoText.isNotBlank()) {
                        todos = todos + Todo(
                            id = todos.size + 1,
                            text = newTodoText
                        )
                        newTodoText = ""
                    }
                }
            ) {
                Text("Añadir")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Todo list
        LazyColumn {
            items(todos, key = { it.id }) { todo ->
                TodoItem(
                    todo = todo,
                    onToggle = {
                        todos = todos.map {
                            if (it.id == todo.id) it.copy(completed = !it.completed)
                            else it
                        }
                    },
                    onDelete = {
                        todos = todos.filter { it.id != todo.id }
                    }
                )
            }
        }

        // Stats
        Spacer(modifier = Modifier.weight(1f))
        TodoStats(
            total = todos.size,
            completed = todos.count { it.completed }
        )
    }
}

@Composable
fun TodoItem(
    todo: Todo,
    onToggle: () -> Unit,
    onDelete: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(
            checked = todo.completed,
            onCheckedChange = { onToggle() }
        )

        Text(
            text = todo.text,
            modifier = Modifier.weight(1f),
            style = if (todo.completed) {
                MaterialTheme.typography.bodyLarge.copy(
                    textDecoration = TextDecoration.LineThrough,
                    color = Color.Gray
                )
            } else {
                MaterialTheme.typography.bodyLarge
            }
        )

        IconButton(onClick = onDelete) {
            Icon(
                imageVector = Icons.Default.Delete,
                contentDescription = "Eliminar",
                tint = Color.Red
            )
        }
    }
}

@Composable
fun TodoStats(total: Int, completed: Int) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceAround
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Total", style = MaterialTheme.typography.labelMedium)
                Text("$total", style = MaterialTheme.typography.headlineMedium)
            }

            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Completadas", style = MaterialTheme.typography.labelMedium)
                Text("$completed", style = MaterialTheme.typography.headlineMedium)
            }

            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Pendientes", style = MaterialTheme.typography.labelMedium)
                Text("${total - completed}", style = MaterialTheme.typography.headlineMedium)
            }
        }
    }
}
```

---

### SwiftUI - @Binding

#### Problema: Estado Duplicado

```swift
// ❌ Mal: Cada componente tiene su propio estado
struct BadExample: View {
    var body: some View {
        VStack {
            CounterDisplay()  // Tiene su propio count
            CounterDisplay()  // Tiene su propio count diferente
        }
    }
}
```

#### Solución: Compartir con @Binding

```swift
// ✅ Bien: Estado compartido
struct GoodExample: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Contador compartido: \(count)")
            CounterButton(count: $count)
            CounterButton(count: $count)
        }
    }
}

struct CounterButton: View {
    @Binding var count: Int

    var body: some View {
        Button("Incrementar (actual: \(count))") {
            count += 1
        }
    }
}
```

#### Ejemplo Completo: Todo List

```swift
struct Todo: Identifiable {
    let id: Int
    var text: String
    var completed: Bool = false
}

struct TodoApp: View {
    @State private var todos = [
        Todo(id: 1, text: "Aprender SwiftUI"),
        Todo(id: 2, text: "Practicar layouts"),
        Todo(id: 3, text: "Crear una app")
    ]
    @State private var newTodoText = ""

    var completedCount: Int {
        todos.filter { $0.completed }.count
    }

    var body: some View {
        VStack(spacing: 0) {
            // Header
            Text("Mis Tareas")
                .font(.largeTitle)
                .fontWeight(.bold)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()

            // Add todo
            HStack {
                TextField("Nueva tarea", text: $newTodoText)
                    .textFieldStyle(.roundedBorder)

                Button("Añadir") {
                    if !newTodoText.isEmpty {
                        todos.append(Todo(
                            id: todos.count + 1,
                            text: newTodoText
                        ))
                        newTodoText = ""
                    }
                }
                .buttonStyle(.borderedProminent)
            }
            .padding(.horizontal)

            // Todo list
            List {
                ForEach($todos) { $todo in
                    TodoRow(todo: $todo, onDelete: {
                        todos.removeAll { $0.id == todo.id }
                    })
                }
            }
            .listStyle(.plain)

            // Stats
            TodoStats(total: todos.count, completed: completedCount)
        }
    }
}

struct TodoRow: View {
    @Binding var todo: Todo
    let onDelete: () -> Void

    var body: some View {
        HStack {
            Button(action: {
                todo.completed.toggle()
            }) {
                Image(systemName: todo.completed ? "checkmark.circle.fill" : "circle")
                    .foregroundColor(todo.completed ? .green : .gray)
            }
            .buttonStyle(.plain)

            Text(todo.text)
                .strikethrough(todo.completed)
                .foregroundColor(todo.completed ? .gray : .primary)

            Spacer()

            Button(action: onDelete) {
                Image(systemName: "trash")
                    .foregroundColor(.red)
            }
            .buttonStyle(.plain)
        }
    }
}

struct TodoStats: View {
    let total: Int
    let completed: Int

    var pending: Int {
        total - completed
    }

    var body: some View {
        HStack {
            Spacer()

            VStack {
                Text("Total")
                    .font(.caption)
                Text("\(total)")
                    .font(.title)
                    .fontWeight(.bold)
            }

            Spacer()

            VStack {
                Text("Completadas")
                    .font(.caption)
                Text("\(completed)")
                    .font(.title)
                    .fontWeight(.bold)
            }

            Spacer()

            VStack {
                Text("Pendientes")
                    .font(.caption)
                Text("\(pending)")
                    .font(.title)
                    .fontWeight(.bold)
            }

            Spacer()
        }
        .padding()
        .background(Color.gray.opacity(0.1))
    }
}
```

---

## 🏗️ Arquitectura MVVM - ViewModel

### Jetpack Compose - ViewModel

#### Setup

```kotlin
dependencies {
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}
```

#### Crear ViewModel

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class CounterUiState(
    val count: Int = 0,
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)

class CounterViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(CounterUiState())
    val uiState: StateFlow<CounterUiState> = _uiState.asStateFlow()

    fun increment() {
        _uiState.value = _uiState.value.copy(
            count = _uiState.value.count + 1
        )
    }

    fun decrement() {
        _uiState.value = _uiState.value.copy(
            count = _uiState.value.count - 1
        )
    }

    fun reset() {
        _uiState.value = CounterUiState()
    }

    // Ejemplo con operación asíncrona
    fun incrementAsync() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            kotlinx.coroutines.delay(1000) // Simular operación
            _uiState.value = _uiState.value.copy(
                count = _uiState.value.count + 1,
                isLoading = false
            )
        }
    }
}
```

#### Usar ViewModel en Composable

```kotlin
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        if (uiState.isLoading) {
            CircularProgressIndicator()
            Spacer(modifier = Modifier.height(16.dp))
        }

        Text(
            text = "Contador: ${uiState.count}",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { viewModel.decrement() }) {
                Text("-")
            }

            Button(onClick = { viewModel.increment() }) {
                Text("+")
            }

            Button(onClick = { viewModel.reset() }) {
                Text("Reset")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = { viewModel.incrementAsync() }) {
            Text("Incrementar Async")
        }

        uiState.errorMessage?.let { error ->
            Spacer(modifier = Modifier.height(16.dp))
            Text(error, color = Color.Red)
        }
    }
}
```

#### Ejemplo Completo: Shopping Cart

```kotlin
data class Product(
    val id: Int,
    val name: String,
    val price: Double
)

data class CartItem(
    val product: Product,
    val quantity: Int = 1
)

data class ShoppingCartUiState(
    val items: List<CartItem> = emptyList(),
    val isLoading: Boolean = false
) {
    val total: Double
        get() = items.sumOf { it.product.price * it.quantity }

    val itemCount: Int
        get() = items.sumOf { it.quantity }
}

class ShoppingCartViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(ShoppingCartUiState())
    val uiState: StateFlow<ShoppingCartUiState> = _uiState.asStateFlow()

    fun addProduct(product: Product) {
        val currentItems = _uiState.value.items
        val existingItem = currentItems.find { it.product.id == product.id }

        val newItems = if (existingItem != null) {
            currentItems.map {
                if (it.product.id == product.id) {
                    it.copy(quantity = it.quantity + 1)
                } else {
                    it
                }
            }
        } else {
            currentItems + CartItem(product)
        }

        _uiState.value = _uiState.value.copy(items = newItems)
    }

    fun removeProduct(productId: Int) {
        val newItems = _uiState.value.items.filter { it.product.id != productId }
        _uiState.value = _uiState.value.copy(items = newItems)
    }

    fun updateQuantity(productId: Int, quantity: Int) {
        if (quantity <= 0) {
            removeProduct(productId)
            return
        }

        val newItems = _uiState.value.items.map {
            if (it.product.id == productId) {
                it.copy(quantity = quantity)
            } else {
                it
            }
        }

        _uiState.value = _uiState.value.copy(items = newItems)
    }

    fun clearCart() {
        _uiState.value = ShoppingCartUiState()
    }
}

@Composable
fun ShoppingCartScreen(viewModel: ShoppingCartViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    Column(modifier = Modifier.fillMaxSize()) {
        // Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Carrito (${uiState.itemCount} items)",
                style = MaterialTheme.typography.headlineMedium
            )

            if (uiState.items.isNotEmpty()) {
                TextButton(onClick = { viewModel.clearCart() }) {
                    Text("Vaciar", color = Color.Red)
                }
            }
        }

        if (uiState.items.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "Carrito vacío",
                    style = MaterialTheme.typography.bodyLarge,
                    color = Color.Gray
                )
            }
        } else {
            // Items list
            LazyColumn(
                modifier = Modifier.weight(1f),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(uiState.items) { item ->
                    CartItemRow(
                        item = item,
                        onQuantityChange = { newQuantity ->
                            viewModel.updateQuantity(item.product.id, newQuantity)
                        },
                        onRemove = {
                            viewModel.removeProduct(item.product.id)
                        }
                    )
                }
            }

            // Total
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Total:",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )

                    Text(
                        text = "$${String.format("%.2f", uiState.total)}",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = Color.Green
                    )
                }
            }

            Button(
                onClick = { /* Checkout */ },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .height(50.dp)
            ) {
                Text("Proceder al Pago")
            }
        }
    }
}

@Composable
fun CartItemRow(
    item: CartItem,
    onQuantityChange: (Int) -> Unit,
    onRemove: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.product.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "$${item.product.price}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color.Gray
                )
            }

            // Quantity controls
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                IconButton(
                    onClick = { onQuantityChange(item.quantity - 1) },
                    enabled = item.quantity > 1
                ) {
                    Icon(Icons.Default.Remove, contentDescription = "Decrease")
                }

                Text(
                    text = item.quantity.toString(),
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.widthIn(min = 30.dp),
                    textAlign = TextAlign.Center
                )

                IconButton(onClick = { onQuantityChange(item.quantity + 1) }) {
                    Icon(Icons.Default.Add, contentDescription = "Increase")
                }

                IconButton(onClick = onRemove) {
                    Icon(
                        Icons.Default.Delete,
                        contentDescription = "Remove",
                        tint = Color.Red
                    )
                }
            }
        }
    }
}
```

---

### SwiftUI - ObservableObject

#### Crear ViewModel

```swift
import Foundation
import Combine

struct CounterUiState {
    var count: Int = 0
    var isLoading: Bool = false
    var errorMessage: String? = nil
}

class CounterViewModel: ObservableObject {
    @Published var uiState = CounterUiState()

    func increment() {
        uiState.count += 1
    }

    func decrement() {
        uiState.count -= 1
    }

    func reset() {
        uiState = CounterUiState()
    }

    func incrementAsync() {
        uiState.isLoading = true

        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.uiState.count += 1
            self.uiState.isLoading = false
        }
    }
}
```

#### Usar ViewModel

```swift
struct CounterScreen: View {
    @StateObject private var viewModel = CounterViewModel()

    var body: some View {
        VStack(spacing: 16) {
            if viewModel.uiState.isLoading {
                ProgressView()
            }

            Text("Contador: \(viewModel.uiState.count)")
                .font(.largeTitle)

            HStack(spacing: 8) {
                Button("-") {
                    viewModel.decrement()
                }

                Button("+") {
                    viewModel.increment()
                }

                Button("Reset") {
                    viewModel.reset()
                }
            }
            .buttonStyle(.bordered)

            Button("Incrementar Async") {
                viewModel.incrementAsync()
            }
            .buttonStyle(.borderedProminent)

            if let error = viewModel.uiState.errorMessage {
                Text(error)
                    .foregroundColor(.red)
            }
        }
    }
}
```

#### Ejemplo Completo: Shopping Cart

```swift
struct Product: Identifiable, Hashable {
    let id: Int
    let name: String
    let price: Double
}

struct CartItem: Identifiable {
    let id = UUID()
    let product: Product
    var quantity: Int = 1
}

class ShoppingCartViewModel: ObservableObject {
    @Published var items: [CartItem] = []

    var total: Double {
        items.reduce(0) { $0 + ($1.product.price * Double($1.quantity)) }
    }

    var itemCount: Int {
        items.reduce(0) { $0 + $1.quantity }
    }

    func addProduct(_ product: Product) {
        if let index = items.firstIndex(where: { $0.product.id == product.id }) {
            items[index].quantity += 1
        } else {
            items.append(CartItem(product: product))
        }
    }

    func removeProduct(_ productId: Int) {
        items.removeAll { $0.product.id == productId }
    }

    func updateQuantity(productId: Int, quantity: Int) {
        if quantity <= 0 {
            removeProduct(productId)
            return
        }

        if let index = items.firstIndex(where: { $0.product.id == productId }) {
            items[index].quantity = quantity
        }
    }

    func clearCart() {
        items.removeAll()
    }
}

struct ShoppingCartScreen: View {
    @StateObject private var viewModel = ShoppingCartViewModel()

    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("Carrito (\(viewModel.itemCount) items)")
                    .font(.title)
                    .fontWeight(.bold)

                Spacer()

                if !viewModel.items.isEmpty {
                    Button("Vaciar") {
                        viewModel.clearCart()
                    }
                    .foregroundColor(.red)
                }
            }
            .padding()

            if viewModel.items.isEmpty {
                Spacer()
                Text("Carrito vacío")
                    .font(.title2)
                    .foregroundColor(.gray)
                Spacer()
            } else {
                // Items list
                List {
                    ForEach(viewModel.items) { item in
                        CartItemRow(
                            item: item,
                            onQuantityChange: { newQuantity in
                                viewModel.updateQuantity(
                                    productId: item.product.id,
                                    quantity: newQuantity
                                )
                            },
                            onRemove: {
                                viewModel.removeProduct(item.product.id)
                            }
                        )
                    }
                }
                .listStyle(.plain)

                // Total
                VStack(spacing: 16) {
                    HStack {
                        Text("Total:")
                            .font(.title2)
                            .fontWeight(.bold)

                        Spacer()

                        Text("$\(viewModel.total, specifier: "%.2f")")
                            .font(.title)
                            .fontWeight(.bold)
                            .foregroundColor(.green)
                    }
                    .padding()
                    .background(Color.blue.opacity(0.1))

                    Button(action: {
                        // Checkout
                    }) {
                        Text("Proceder al Pago")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    .padding(.horizontal)
                }
            }
        }
    }
}

struct CartItemRow: View {
    let item: CartItem
    let onQuantityChange: (Int) -> Void
    let onRemove: () -> Void

    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(item.product.name)
                    .font(.headline)
                Text("$\(item.product.price, specifier: "%.2f")")
                    .foregroundColor(.gray)
            }

            Spacer()

            HStack(spacing: 12) {
                Button(action: {
                    onQuantityChange(item.quantity - 1)
                }) {
                    Image(systemName: "minus.circle")
                }
                .disabled(item.quantity <= 1)

                Text("\(item.quantity)")
                    .frame(minWidth: 30)

                Button(action: {
                    onQuantityChange(item.quantity + 1)
                }) {
                    Image(systemName: "plus.circle")
                }

                Button(action: onRemove) {
                    Image(systemName: "trash")
                        .foregroundColor(.red)
                }
            }
        }
    }
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear una app de notas con MVVM.

### Requisitos

**Modelo:**
- `Note(id, title, content, createdAt, isPinned)`

**ViewModel:**
- Lista de notas
- Agregar nota
- Editar nota
- Eliminar nota
- Marcar como favorita

**UI:**
- Lista de notas
- Formulario para crear/editar
- Filtrar por favoritas
- Buscar notas

### Bonus

- Ordenar por fecha/título
- Contador de palabras
- Categorías/tags
- Modo oscuro

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **State**: [developer.android.com/jetpack/compose/state](https://developer.android.com/jetpack/compose/state)
- **ViewModel**: [developer.android.com/topic/libraries/architecture/viewmodel](https://developer.android.com/topic/libraries/architecture/viewmodel)
- **StateFlow**: [developer.android.com/kotlin/flow/stateflow-and-sharedflow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)

### SwiftUI
- **State**: [developer.apple.com/documentation/swiftui/state](https://developer.apple.com/documentation/swiftui/state)
- **ObservableObject**: [developer.apple.com/documentation/combine/observableobject](https://developer.apple.com/documentation/combine/observableobject)
- **Binding**: [developer.apple.com/documentation/swiftui/binding](https://developer.apple.com/documentation/swiftui/binding)

---

**Anterior:** [06_NAVEGACION.md](06_NAVEGACION.md)
**Siguiente:** [08_FORMULARIOS.md](08_FORMULARIOS.md) - Formularios y validación

