# 📱 Introducción a UI Declarativa

> **Jetpack Compose (Android) & SwiftUI (iOS) - Paradigma Declarativo**

---

## 🎯 Objetivo

Entender qué es la UI declarativa, cómo se diferencia de la UI imperativa tradicional, y por qué tanto Android como iOS adoptaron este paradigma.

---

## 📚 ¿Qué es UI Declarativa?

### Definición

**UI Declarativa** es un paradigma de programación donde describes **QUÉ** quieres mostrar en la pantalla, no **CÓMO** construirlo paso a paso.

```
UI Imperativa: "Crea un botón, agrégalo al layout, configura su color, posición..."
UI Declarativa: "Quiero un botón azul con texto 'Click'"
```

### Analogía del Restaurante

**Imperativo (Tradicional):**
```
1. Ve a la cocina
2. Toma una sartén
3. Enciende la estufa
4. Corta las verduras
5. Cocina por 10 minutos
6. Sirve en un plato
```

**Declarativo (Moderno):**
```
"Quiero un plato de pasta con verduras"
```

El framework (el chef) se encarga de los detalles de implementación.

---

## 🔄 UI Imperativa vs Declarativa

### UI Imperativa (Tradicional)

#### Android (XML + Java/Kotlin)

```xml
<!-- activity_main.xml -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Contador: 0"
        android:textSize="24sp"/>

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Incrementar"/>
</LinearLayout>
```

```kotlin
// MainActivity.kt
class MainActivity : AppCompatActivity() {
    private var counter = 0
    private lateinit var textView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 1. Encontrar vistas
        textView = findViewById(R.id.textView)
        val button = findViewById<Button>(R.id.button)

        // 2. Configurar listeners
        button.setOnClickListener {
            counter++
            // 3. Actualizar manualmente
            textView.text = "Contador: $counter"
        }
    }
}
```

**Problemas:**
- 😰 Muchos pasos manuales
- 😰 Fácil olvidar actualizar la UI
- 😰 Código separado (XML + Kotlin)
- 😰 Referencias nulas (`findViewById`)
- 😰 Estado y UI desincronizados

#### iOS (UIKit + Swift)

```swift
// ViewController.swift
class ViewController: UIViewController {
    private var counter = 0
    private var label: UILabel!
    private var button: UIButton!

    override func viewDidLoad() {
        super.viewDidLoad()

        // 1. Crear vistas manualmente
        label = UILabel()
        label.text = "Contador: 0"
        label.font = UIFont.systemFont(ofSize: 24)
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)

        button = UIButton(type: .system)
        button.setTitle("Incrementar", for: .normal)
        button.translatesAutoresizingMaskIntoConstraints = false
        button.addTarget(self, action: #selector(buttonTapped), for: .touchUpInside)
        view.addSubview(button)

        // 2. Configurar constraints manualmente
        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor, constant: -50),
            button.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            button.topAnchor.constraint(equalTo: label.bottomAnchor, constant: 20)
        ])
    }

    @objc func buttonTapped() {
        counter += 1
        // 3. Actualizar manualmente
        label.text = "Contador: \(counter)"
    }
}
```

**Problemas similares:**
- 😰 Configuración manual de constraints
- 😰 Callbacks imperativos (`@objc`)
- 😰 Mucho código boilerplate
- 😰 Actualización manual de UI

---

### UI Declarativa (Moderna)

#### Android (Jetpack Compose)

```kotlin
@Composable
fun CounterScreen() {
    // 1. Estado reactivo
    var counter by remember { mutableStateOf(0) }

    // 2. Describe la UI
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Contador: $counter",
            fontSize = 24.sp
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = { counter++ }) {
            Text("Incrementar")
        }
    }
    // 3. La UI se actualiza automáticamente
}
```

**Ventajas:**
- ✅ Todo en Kotlin (un solo lenguaje)
- ✅ Estado reactivo automático
- ✅ Menos código
- ✅ Sin referencias nulas
- ✅ UI siempre sincronizada con el estado

#### iOS (SwiftUI)

```swift
struct CounterView: View {
    // 1. Estado reactivo
    @State private var counter = 0

    // 2. Describe la UI
    var body: some View {
        VStack(spacing: 16) {
            Text("Contador: \(counter)")
                .font(.title)

            Button("Incrementar") {
                counter += 1
            }
        }
    }
    // 3. La UI se actualiza automáticamente
}
```

**Ventajas idénticas:**
- ✅ Todo en Swift (un solo lenguaje)
- ✅ Estado reactivo automático
- ✅ Código conciso
- ✅ Sin opcionales problemáticos
- ✅ UI siempre sincronizada

---

## 🧠 Conceptos Clave

### 1. Estado Reactivo

El framework observa automáticamente los cambios en el estado y re-renderiza la UI.

#### Jetpack Compose

```kotlin
@Composable
fun ReactiveExample() {
    var isHappy by remember { mutableStateOf(true) }

    Column {
        // La UI se actualiza automáticamente cuando cambia isHappy
        Text(if (isHappy) "😊" else "😢")

        Button(onClick = { isHappy = !isHappy }) {
            Text("Cambiar Estado")
        }
    }
}
```

#### SwiftUI

```swift
struct ReactiveExample: View {
    @State private var isHappy = true

    var body: some View {
        VStack {
            // La UI se actualiza automáticamente cuando cambia isHappy
            Text(isHappy ? "😊" : "😢")

            Button("Cambiar Estado") {
                isHappy.toggle()
            }
        }
    }
}
```

### 2. Composición sobre Herencia

En lugar de heredar de clases base complejas, **compones** UI combinando funciones pequeñas.

#### Jetpack Compose

```kotlin
@Composable
fun UserCard(name: String, age: Int) {
    Card {
        Column(modifier = Modifier.padding(16.dp)) {
            UserAvatar()
            UserInfo(name, age)
            UserActions()
        }
    }
}

@Composable
fun UserAvatar() { /* ... */ }

@Composable
fun UserInfo(name: String, age: Int) { /* ... */ }

@Composable
fun UserActions() { /* ... */ }
```

#### SwiftUI

```swift
struct UserCard: View {
    let name: String
    let age: Int

    var body: some View {
        VStack(spacing: 8) {
            UserAvatar()
            UserInfo(name: name, age: age)
            UserActions()
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
    }
}

struct UserAvatar: View { /* ... */ }
struct UserInfo: View { /* ... */ }
struct UserActions: View { /* ... */ }
```

### 3. Single Source of Truth

El estado vive en **un solo lugar**, y la UI se deriva de ese estado.

#### Jetpack Compose

```kotlin
@Composable
fun TodoApp() {
    // ✅ Una sola fuente de verdad
    var todos by remember { mutableStateOf(listOf<String>()) }

    Column {
        TodoList(todos = todos)
        AddTodoButton(onAdd = { newTodo ->
            todos = todos + newTodo  // Actualizar estado
        })
    }
    // La UI se actualiza automáticamente
}
```

#### SwiftUI

```swift
struct TodoApp: View {
    // ✅ Una sola fuente de verdad
    @State private var todos: [String] = []

    var body: some View {
        VStack {
            TodoList(todos: todos)
            AddTodoButton { newTodo in
                todos.append(newTodo)  // Actualizar estado
            }
        }
        // La UI se actualiza automáticamente
    }
}
```

---

## 📊 Comparación Directa

| Aspecto | Imperativo (Tradicional) | Declarativo (Moderno) |
|---------|-------------------------|----------------------|
| **Paradigma** | "CÓMO hacerlo" | "QUÉ mostrar" |
| **Lenguajes** | XML + Kotlin / Storyboards + Swift | Kotlin puro / Swift puro |
| **Actualización UI** | Manual (`textView.text = ...`) | Automática (reactiva) |
| **Estado** | Múltiples fuentes | Single source of truth |
| **Composición** | Herencia de clases | Funciones componibles |
| **Código** | Verbose, boilerplate | Conciso, expresivo |
| **Debugging** | Difícil (estado distribuido) | Más fácil (estado centralizado) |
| **Testing** | Complicado (UI + lógica mezclada) | Más simple (funciones puras) |
| **Performance** | Manual optimization | Smart recomposition |
| **Learning Curve** | Empinada | Más natural |

---

## ✅ Ventajas de UI Declarativa

### 1. Menos Código, Más Claro

**Imperativo:**
```kotlin
// 50 líneas de XML + 30 líneas de Kotlin = 80 líneas
```

**Declarativo:**
```kotlin
// 20 líneas de Kotlin = 20 líneas
```

### 2. UI Siempre Sincronizada

```kotlin
// ❌ Imperativo: Puedes olvidar actualizar
button.setOnClickListener {
    counter++
    // Olvidé actualizar textView.text!
}

// ✅ Declarativo: Actualización automática
Button(onClick = { counter++ }) {
    Text("Contador: $counter")  // Se actualiza solo
}
```

### 3. Más Fácil de Razonar

```kotlin
// La UI es una función del estado
UI = f(State)
```

Si el estado es `counter = 5`, la UI **siempre** mostrará "Contador: 5". No hay confusión.

### 4. Reutilización

```kotlin
@Composable
fun StyledButton(text: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary
        )
    ) {
        Text(text)
    }
}

// Reutilizar en cualquier lugar
StyledButton("Login") { /* ... */ }
StyledButton("Register") { /* ... */ }
```

---

## ⚠️ Desventajas y Consideraciones

### 1. Curva de Aprendizaje Inicial

Requiere **cambio de mentalidad**:
- Pensar en términos de "estado → UI"
- Entender recomposición (Compose) o re-renderizado (SwiftUI)

### 2. Performance en Listas Grandes

Requiere entender optimizaciones:
- `LazyColumn` (Compose) vs `List` (SwiftUI)
- Claves estables para items
- Evitar recomposiciones innecesarias

### 3. Interoperabilidad

Si tienes código legacy:
- Compose puede coexistir con Views XML
- SwiftUI puede coexistir con UIKit
- Pero requiere puentes (bridges)

### 4. Tooling y Debug

Las herramientas están madurando:
- Layout Inspector en Android Studio
- Xcode Previews
- Pero aún hay espacio para mejorar

---

## 🎨 ¿Por Qué Ambas Plataformas Adoptaron Este Paradigma?

### 1. Influencia de React

React.js popularizó el paradigma declarativo en web (2013). Ambas plataformas se inspiraron:

```jsx
// React (2013)
function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

### 2. Tendencias de la Industria

Flutter (Google), React Native (Meta), Vue.js... todos son declarativos.

### 3. Mejor Developer Experience

Los desarrolladores son más productivos con menos código y menos bugs.

### 4. Adaptación a Múltiples Dispositivos

Más fácil adaptar UI a diferentes tamaños de pantalla, orientaciones, dark mode, etc.

---

## 🚀 Ejemplo Completo Comparativo

### Problema: Lista de Tareas con Filtros

#### Jetpack Compose

```kotlin
enum class Filter { ALL, ACTIVE, COMPLETED }

@Composable
fun TodoApp() {
    var todos by remember { mutableStateOf(listOf<Todo>()) }
    var filter by remember { mutableStateOf(Filter.ALL) }

    Column {
        // Filtros
        Row {
            FilterChip("Todas", filter == Filter.ALL) { filter = Filter.ALL }
            FilterChip("Activas", filter == Filter.ACTIVE) { filter = Filter.ACTIVE }
            FilterChip("Completadas", filter == Filter.COMPLETED) { filter = Filter.COMPLETED }
        }

        // Lista filtrada (se actualiza automáticamente)
        val filteredTodos = when (filter) {
            Filter.ALL -> todos
            Filter.ACTIVE -> todos.filter { !it.completed }
            Filter.COMPLETED -> todos.filter { it.completed }
        }

        LazyColumn {
            items(filteredTodos) { todo ->
                TodoItem(todo) { completed ->
                    todos = todos.map {
                        if (it.id == todo.id) it.copy(completed = completed) else it
                    }
                }
            }
        }
    }
}
```

#### SwiftUI

```swift
enum Filter { case all, active, completed }

struct TodoApp: View {
    @State private var todos: [Todo] = []
    @State private var filter: Filter = .all

    var body: some View {
        VStack {
            // Filtros
            Picker("Filter", selection: $filter) {
                Text("Todas").tag(Filter.all)
                Text("Activas").tag(Filter.active)
                Text("Completadas").tag(Filter.completed)
            }
            .pickerStyle(.segmented)

            // Lista filtrada (se actualiza automáticamente)
            List(filteredTodos) { todo in
                TodoRow(todo: todo) { completed in
                    if let index = todos.firstIndex(where: { $0.id == todo.id }) {
                        todos[index].completed = completed
                    }
                }
            }
        }
    }

    var filteredTodos: [Todo] {
        switch filter {
        case .all: return todos
        case .active: return todos.filter { !$0.completed }
        case .completed: return todos.filter { $0.completed }
        }
    }
}
```

**Nota:** Ambas implementaciones son:
- ✅ Reactivas
- ✅ Concisas
- ✅ Fáciles de entender
- ✅ Sin código boilerplate

---

## 🎯 Conclusiones

### UI Declarativa es el Futuro

Ambas plataformas han invertido fuertemente en este paradigma:
- **Compose** es el estándar oficial para Android
- **SwiftUI** es el estándar oficial para iOS

### Cambio de Mentalidad

```
Deja de pensar en:        Empieza a pensar en:
─────────────────────     ────────────────────
"Cómo construir la UI"    "Qué mostrar en la UI"
"Actualizar vistas"       "Cambiar el estado"
"Listeners y callbacks"   "Funciones reactivas"
```

### Similitudes Entre Compose y SwiftUI

| Concepto | Compose | SwiftUI |
|----------|---------|---------|
| Contenedor vertical | `Column` | `VStack` |
| Contenedor horizontal | `Row` | `HStack` |
| Estado local | `remember { mutableStateOf() }` | `@State` |
| Texto | `Text()` | `Text()` |
| Botón | `Button()` | `Button()` |
| Lista | `LazyColumn` | `List` |

**Son MUY similares. Aprender uno facilita aprender el otro.**

---

## 📝 Ejercicio Práctico

### Objetivo

Crear una app de contador simple en ambas plataformas.

### Requisitos

- Mostrar un número (empieza en 0)
- Botón "Incrementar" (+1)
- Botón "Decrementar" (-1)
- Botón "Reset" (volver a 0)
- Cambiar color del número según su valor:
  - Verde si > 0
  - Rojo si < 0
  - Gris si = 0

### Template Jetpack Compose

```kotlin
@Composable
fun CounterApp() {
    var counter by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // TODO: Mostrar el número con color

        // TODO: Botón incrementar

        // TODO: Botón decrementar

        // TODO: Botón reset
    }
}
```

### Template SwiftUI

```swift
struct CounterApp: View {
    @State private var counter = 0

    var body: some View {
        VStack(spacing: 20) {
            // TODO: Mostrar el número con color

            // TODO: Botón incrementar

            // TODO: Botón decrementar

            // TODO: Botón reset
        }
    }
}
```

### Solución

Intenta resolverlo primero. La solución estará en el siguiente documento.

---

## 🔗 Recursos Adicionales

- **Jetpack Compose**: [developer.android.com/jetpack/compose](https://developer.android.com/jetpack/compose)
- **SwiftUI**: [developer.apple.com/xcode/swiftui/](https://developer.apple.com/xcode/swiftui/)
- **Thinking in Compose**: [developer.android.com/jetpack/compose/mental-model](https://developer.android.com/jetpack/compose/mental-model)
- **SwiftUI Tutorials**: [developer.apple.com/tutorials/swiftui](https://developer.apple.com/tutorials/swiftui)

---

**Siguiente:** [02_SETUP_AMBIENTE.md](02_SETUP_AMBIENTE.md) - Configuración del ambiente de desarrollo

