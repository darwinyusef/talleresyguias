# 📋 Listas y Grids

> **Jetpack Compose (Android) & SwiftUI (iOS) - Colecciones de Datos**

---

## 🎯 Objetivo

Dominar la creación de listas y grids eficientes para mostrar colecciones de datos dinámicos.

---

## 📚 Conceptos Fundamentales

### ¿Por qué Listas Lazy?

Las listas tradicionales cargan **todos** los elementos en memoria, incluso los que no están visibles.

Las **Lazy Lists** (listas perezosas) solo cargan los elementos visibles en pantalla, mejorando el performance dramáticamente.

| Tipo | Carga | Performance | Uso |
|------|-------|-------------|-----|
| **Lista Normal** | Todos los items | ❌ Malo con 100+ items | Listas pequeñas (<20) |
| **Lazy List** | Solo items visibles | ✅ Excelente con miles | Listas grandes |

---

## 📜 LazyColumn / List - Lista Vertical

### Jetpack Compose - LazyColumn

#### Uso Básico

```kotlin
@Composable
fun SimpleLazyColumn() {
    LazyColumn {
        // items individuales
        item {
            Text("Header")
        }

        // Múltiples items desde una lista
        items(10) { index ->
            Text("Item $index")
        }

        item {
            Text("Footer")
        }
    }
}
```

#### Lista desde Datos

```kotlin
data class User(val id: Int, val name: String, val email: String)

@Composable
fun UserList() {
    val users = remember {
        listOf(
            User(1, "Juan Pérez", "juan@example.com"),
            User(2, "María García", "maria@example.com"),
            User(3, "Carlos López", "carlos@example.com"),
            User(4, "Ana Martínez", "ana@example.com"),
            User(5, "Luis Rodríguez", "luis@example.com")
        )
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(users) { user ->
            UserItem(user)
        }
    }
}

@Composable
fun UserItem(user: User) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Avatar
            Box(
                modifier = Modifier
                    .size(50.dp)
                    .background(Color.Blue, shape = CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = user.name.first().toString(),
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 20.sp
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            // Info
            Column {
                Text(
                    text = user.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = user.email,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )
            }
        }
    }
}
```

#### Items con Clave (Key)

Las claves ayudan a Compose a identificar items únicos y optimizar recomposiciones:

```kotlin
@Composable
fun UserListWithKeys() {
    val users = remember { getUserList() }

    LazyColumn {
        items(
            items = users,
            key = { user -> user.id }  // ← Importante para performance
        ) { user ->
            UserItem(user)
        }
    }
}
```

#### LazyColumn con Secciones

```kotlin
@Composable
fun SectionedList() {
    val grouped = mapOf(
        "A" to listOf("Ana", "Antonio", "Andrea"),
        "B" to listOf("Beatriz", "Bruno"),
        "C" to listOf("Carlos", "Carmen", "Cristina")
    )

    LazyColumn {
        grouped.forEach { (letter, names) ->
            // Header de sección
            item {
                Text(
                    text = letter,
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.LightGray)
                        .padding(16.dp)
                )
            }

            // Items de la sección
            items(names) { name ->
                Text(
                    text = name,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp)
                )
                Divider()
            }
        }
    }
}
```

#### Lista con Click

```kotlin
@Composable
fun ClickableList() {
    val items = remember { (1..20).toList() }
    var selectedItem by remember { mutableStateOf<Int?>(null) }

    LazyColumn {
        items(items) { item ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
                    .clickable { selectedItem = item },
                colors = CardDefaults.cardColors(
                    containerColor = if (selectedItem == item) Color.Blue.copy(alpha = 0.2f)
                    else Color.White
                )
            ) {
                Text(
                    text = "Item $item",
                    modifier = Modifier.padding(16.dp),
                    fontWeight = if (selectedItem == item) FontWeight.Bold else FontWeight.Normal
                )
            }
        }
    }

    // Mostrar selección
    selectedItem?.let {
        Text("Seleccionado: Item $it")
    }
}
```

---

### SwiftUI - List

#### Uso Básico

```swift
struct SimpleList: View {
    var body: some View {
        List {
            Text("Header")

            ForEach(0..<10) { index in
                Text("Item \(index)")
            }

            Text("Footer")
        }
    }
}
```

#### Lista desde Datos

```swift
struct User: Identifiable {
    let id: Int
    let name: String
    let email: String
}

struct UserList: View {
    let users = [
        User(id: 1, name: "Juan Pérez", email: "juan@example.com"),
        User(id: 2, name: "María García", email: "maria@example.com"),
        User(id: 3, name: "Carlos López", email: "carlos@example.com"),
        User(id: 4, name: "Ana Martínez", email: "ana@example.com"),
        User(id: 5, name: "Luis Rodríguez", email: "luis@example.com")
    ]

    var body: some View {
        List(users) { user in
            UserRow(user: user)
        }
    }
}

struct UserRow: View {
    let user: User

    var body: some View {
        HStack(spacing: 16) {
            // Avatar
            ZStack {
                Circle()
                    .fill(Color.blue)
                    .frame(width: 50, height: 50)

                Text(String(user.name.prefix(1)))
                    .foregroundColor(.white)
                    .fontWeight(.bold)
                    .font(.title2)
            }

            // Info
            VStack(alignment: .leading, spacing: 4) {
                Text(user.name)
                    .font(.headline)
                    .fontWeight(.bold)

                Text(user.email)
                    .font(.subheadline)
                    .foregroundColor(.gray)
            }
        }
        .padding(.vertical, 4)
    }
}
```

#### Lista con Secciones

```swift
struct SectionedList: View {
    let grouped = [
        "A": ["Ana", "Antonio", "Andrea"],
        "B": ["Beatriz", "Bruno"],
        "C": ["Carlos", "Carmen", "Cristina"]
    ]

    var body: some View {
        List {
            ForEach(grouped.keys.sorted(), id: \.self) { letter in
                Section(header: Text(letter).font(.headline)) {
                    ForEach(grouped[letter]!, id: \.self) { name in
                        Text(name)
                    }
                }
            }
        }
    }
}
```

#### Lista con Click

```swift
struct ClickableList: View {
    let items = Array(1...20)
    @State private var selectedItem: Int?

    var body: some View {
        VStack {
            List(items, id: \.self) { item in
                HStack {
                    Text("Item \(item)")
                        .fontWeight(selectedItem == item ? .bold : .regular)

                    Spacer()

                    if selectedItem == item {
                        Image(systemName: "checkmark")
                            .foregroundColor(.blue)
                    }
                }
                .contentShape(Rectangle())
                .onTapGesture {
                    selectedItem = item
                }
                .listRowBackground(
                    selectedItem == item ? Color.blue.opacity(0.2) : Color.clear
                )
            }

            if let selected = selectedItem {
                Text("Seleccionado: Item \(selected)")
                    .padding()
            }
        }
    }
}
```

#### Estilos de Lista

```swift
struct ListStyles: View {
    var body: some View {
        VStack {
            // Inset Style
            List {
                Text("Item 1")
                Text("Item 2")
            }
            .listStyle(.inset)

            // Grouped Style
            List {
                Text("Item 1")
                Text("Item 2")
            }
            .listStyle(.grouped)

            // Plain Style
            List {
                Text("Item 1")
                Text("Item 2")
            }
            .listStyle(.plain)

            // Sidebar Style
            List {
                Text("Item 1")
                Text("Item 2")
            }
            .listStyle(.sidebar)
        }
    }
}
```

---

### Comparación LazyColumn / List

| Feature | Compose (LazyColumn) | SwiftUI (List) |
|---------|----------------------|----------------|
| Básico | `LazyColumn { items(list) { } }` | `List(list) { }` |
| Con clave | `items(list, key = { it.id })` | Struct con `Identifiable` |
| Espaciado | `verticalArrangement = Arrangement.spacedBy(8.dp)` | `List { }.listRowSpacing(8)` |
| Padding | `contentPadding = PaddingValues(16.dp)` | `.padding()` en items |
| Secciones | Manual con `item { }` para headers | `Section(header:) { }` nativo |
| Click | `.clickable { }` en item | `.onTapGesture { }` |

---

## ↔️ LazyRow / ScrollView - Lista Horizontal

### Jetpack Compose - LazyRow

```kotlin
@Composable
fun HorizontalList() {
    val colors = listOf(Color.Red, Color.Green, Color.Blue, Color.Yellow, Color.Magenta)

    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(colors) { color ->
            Box(
                modifier = Modifier
                    .size(150.dp, 200.dp)
                    .background(color, shape = RoundedCornerShape(12.dp))
            )
        }
    }
}

// Ejemplo: Categorías horizontales
@Composable
fun CategoryRow() {
    val categories = listOf(
        "Tecnología" to "💻",
        "Deportes" to "⚽",
        "Música" to "🎵",
        "Comida" to "🍕",
        "Viajes" to "✈️"
    )

    LazyRow(
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(categories) { (name, emoji) ->
            CategoryChip(name, emoji)
        }
    }
}

@Composable
fun CategoryChip(name: String, emoji: String) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color(0xFF6200EE))
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(emoji, fontSize = 24.sp)
            Spacer(modifier = Modifier.width(8.dp))
            Text(name, color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
}
```

---

### SwiftUI - ScrollView Horizontal

```swift
struct HorizontalList: View {
    let colors: [Color] = [.red, .green, .blue, .yellow, .purple]

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(0..<colors.count, id: \.self) { index in
                    RoundedRectangle(cornerRadius: 12)
                        .fill(colors[index])
                        .frame(width: 150, height: 200)
                }
            }
            .padding(.horizontal, 16)
        }
    }
}

// Ejemplo: Categorías horizontales
struct CategoryRow: View {
    let categories = [
        ("Tecnología", "💻"),
        ("Deportes", "⚽"),
        ("Música", "🎵"),
        ("Comida", "🍕"),
        ("Viajes", "✈️")
    ]

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(categories, id: \.0) { name, emoji in
                    CategoryChip(name: name, emoji: emoji)
                }
            }
            .padding(.horizontal, 16)
        }
    }
}

struct CategoryChip: View {
    let name: String
    let emoji: String

    var body: some View {
        HStack(spacing: 8) {
            Text(emoji)
                .font(.title2)
            Text(name)
                .fontWeight(.bold)
                .foregroundColor(.white)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(Color.purple)
        .cornerRadius(20)
    }
}
```

---

## 🎯 LazyVerticalGrid / LazyVGrid - Grids

### Jetpack Compose - LazyVerticalGrid

#### Grid de Columnas Fijas

```kotlin
@Composable
fun SimpleGrid() {
    val items = (1..20).toList()

    LazyVerticalGrid(
        columns = GridCells.Fixed(3),  // 3 columnas
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(items) { number ->
            Box(
                modifier = Modifier
                    .aspectRatio(1f)  // Cuadrado
                    .background(Color.Blue, shape = RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = number.toString(),
                    color = Color.White,
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}
```

#### Grid Adaptativo (según ancho)

```kotlin
@Composable
fun AdaptiveGrid() {
    val items = (1..50).toList()

    LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = 100.dp),  // Mín 100dp por item
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(items) { number ->
            Box(
                modifier = Modifier
                    .aspectRatio(1f)
                    .background(Color.Green, shape = RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = number.toString(),
                    color = Color.White,
                    fontSize = 20.sp
                )
            }
        }
    }
}
```

#### Grid de Fotos (Instagram Style)

```kotlin
data class Photo(val id: Int, val color: Color)

@Composable
fun PhotoGrid() {
    val photos = remember {
        (1..30).map {
            Photo(it, Color(Random.nextFloat(), Random.nextFloat(), Random.nextFloat()))
        }
    }

    LazyVerticalGrid(
        columns = GridCells.Fixed(3),
        horizontalArrangement = Arrangement.spacedBy(2.dp),
        verticalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        items(photos, key = { it.id }) { photo ->
            Box(
                modifier = Modifier
                    .aspectRatio(1f)
                    .background(photo.color)
                    .clickable { /* Abrir foto */ }
            )
        }
    }
}
```

#### Grid con Items de Diferente Tamaño (Span)

```kotlin
@Composable
fun StaggeredGrid() {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item(span = { GridItemSpan(2) }) {  // Ocupa 2 columnas
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(100.dp)
                    .background(Color.Red, shape = RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text("Header - Ancho completo", color = Color.White, fontWeight = FontWeight.Bold)
            }
        }

        items(10) { index ->
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(150.dp)
                    .background(Color.Blue, shape = RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text("Item $index", color = Color.White)
            }
        }
    }
}
```

---

### SwiftUI - LazyVGrid

#### Grid de Columnas Fijas

```swift
struct SimpleGrid: View {
    let items = Array(1...20)

    let columns = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 8) {
                ForEach(items, id: \.self) { number in
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.blue)
                        .aspectRatio(1, contentMode: .fit)
                        .overlay(
                            Text("\(number)")
                                .font(.title)
                                .fontWeight(.bold)
                                .foregroundColor(.white)
                        )
                }
            }
            .padding(16)
        }
    }
}
```

#### Grid Adaptativo

```swift
struct AdaptiveGrid: View {
    let items = Array(1...50)

    let columns = [
        GridItem(.adaptive(minimum: 100))  // Mínimo 100pt por item
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 8) {
                ForEach(items, id: \.self) { number in
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.green)
                        .aspectRatio(1, contentMode: .fit)
                        .overlay(
                            Text("\(number)")
                                .font(.title2)
                                .foregroundColor(.white)
                        )
                }
            }
            .padding(16)
        }
    }
}
```

#### Grid de Fotos (Instagram Style)

```swift
struct Photo: Identifiable {
    let id: Int
    let color: Color
}

struct PhotoGrid: View {
    let photos = (1...30).map {
        Photo(id: $0, color: Color(
            red: .random(in: 0...1),
            green: .random(in: 0...1),
            blue: .random(in: 0...1)
        ))
    }

    let columns = [
        GridItem(.flexible(), spacing: 2),
        GridItem(.flexible(), spacing: 2),
        GridItem(.flexible(), spacing: 2)
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 2) {
                ForEach(photos) { photo in
                    Rectangle()
                        .fill(photo.color)
                        .aspectRatio(1, contentMode: .fit)
                        .onTapGesture {
                            // Abrir foto
                        }
                }
            }
        }
    }
}
```

#### Grid Mixto (diferentes tamaños)

```swift
struct MixedGrid: View {
    var body: some View {
        ScrollView {
            LazyVGrid(
                columns: [GridItem(.flexible()), GridItem(.flexible())],
                spacing: 8
            ) {
                // Header ancho completo
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.red)
                    .frame(height: 100)
                    .gridCellColumns(2)  // iOS 16+
                    .overlay(
                        Text("Header - Ancho completo")
                            .foregroundColor(.white)
                            .fontWeight(.bold)
                    )

                // Items normales
                ForEach(0..<10) { index in
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.blue)
                        .frame(height: 150)
                        .overlay(
                            Text("Item \(index)")
                                .foregroundColor(.white)
                        )
                }
            }
            .padding(16)
        }
    }
}
```

---

### Comparación LazyVerticalGrid / LazyVGrid

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Columnas fijas | `GridCells.Fixed(3)` | `[GridItem(.flexible())] x 3` |
| Adaptativo | `GridCells.Adaptive(minSize = 100.dp)` | `[GridItem(.adaptive(minimum: 100))]` |
| Espaciado | `horizontalArrangement/verticalArrangement` | `spacing:` parameter |
| Item span | `item(span = { GridItemSpan(2) })` | `.gridCellColumns(2)` (iOS 16+) |

---

## 🎨 Ejemplo Completo: App de Galería

### Jetpack Compose

```kotlin
data class GalleryItem(
    val id: Int,
    val title: String,
    val color: Color,
    val isFavorite: Boolean = false
)

@Composable
fun GalleryApp() {
    var viewMode by remember { mutableStateOf(ViewMode.GRID) }
    var items by remember {
        mutableStateOf(
            (1..30).map {
                GalleryItem(
                    id = it,
                    title = "Item $it",
                    color = Color(Random.nextFloat(), Random.nextFloat(), Random.nextFloat())
                )
            }
        )
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Top Bar
        TopAppBar(
            title = { Text("Galería") },
            actions = {
                // Toggle view mode
                IconButton(onClick = {
                    viewMode = if (viewMode == ViewMode.GRID) ViewMode.LIST else ViewMode.GRID
                }) {
                    Icon(
                        imageVector = if (viewMode == ViewMode.GRID) Icons.Default.List
                        else Icons.Default.GridView,
                        contentDescription = "Toggle view"
                    )
                }
            }
        )

        // Content
        when (viewMode) {
            ViewMode.LIST -> {
                LazyColumn(
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(items, key = { it.id }) { item ->
                        GalleryListItem(
                            item = item,
                            onFavoriteClick = {
                                items = items.map {
                                    if (it.id == item.id) it.copy(isFavorite = !it.isFavorite)
                                    else it
                                }
                            }
                        )
                    }
                }
            }
            ViewMode.GRID -> {
                LazyVerticalGrid(
                    columns = GridCells.Fixed(2),
                    contentPadding = PaddingValues(16.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(items, key = { it.id }) { item ->
                        GalleryGridItem(
                            item = item,
                            onFavoriteClick = {
                                items = items.map {
                                    if (it.id == item.id) it.copy(isFavorite = !it.isFavorite)
                                    else it
                                }
                            }
                        )
                    }
                }
            }
        }
    }
}

enum class ViewMode { LIST, GRID }

@Composable
fun GalleryListItem(item: GalleryItem, onFavoriteClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .background(item.color, shape = RoundedCornerShape(8.dp))
            )

            Spacer(modifier = Modifier.width(16.dp))

            Text(
                text = item.title,
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.weight(1f)
            )

            IconButton(onClick = onFavoriteClick) {
                Icon(
                    imageVector = if (item.isFavorite) Icons.Default.Favorite
                    else Icons.Default.FavoriteBorder,
                    contentDescription = "Favorite",
                    tint = if (item.isFavorite) Color.Red else Color.Gray
                )
            }
        }
    }
}

@Composable
fun GalleryGridItem(item: GalleryItem, onFavoriteClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Box {
            Column {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f)
                        .background(item.color)
                )

                Text(
                    text = item.title,
                    style = MaterialTheme.typography.bodyMedium,
                    modifier = Modifier.padding(8.dp)
                )
            }

            // Favorite button overlay
            IconButton(
                onClick = onFavoriteClick,
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(4.dp)
            ) {
                Icon(
                    imageVector = if (item.isFavorite) Icons.Default.Favorite
                    else Icons.Default.FavoriteBorder,
                    contentDescription = "Favorite",
                    tint = if (item.isFavorite) Color.Red else Color.White
                )
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun GalleryAppPreview() {
    GalleryApp()
}
```

---

### SwiftUI

```swift
struct GalleryItem: Identifiable {
    let id: Int
    let title: String
    let color: Color
    var isFavorite: Bool = false
}

enum ViewMode {
    case list, grid
}

struct GalleryApp: View {
    @State private var viewMode: ViewMode = .grid
    @State private var items = (1...30).map {
        GalleryItem(
            id: $0,
            title: "Item \($0)",
            color: Color(
                red: .random(in: 0...1),
                green: .random(in: 0...1),
                blue: .random(in: 0...1)
            )
        )
    }

    let columns = [
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    var body: some View {
        NavigationView {
            ScrollView {
                switch viewMode {
                case .list:
                    LazyVStack(spacing: 8) {
                        ForEach(items) { item in
                            GalleryListRow(item: item) {
                                toggleFavorite(id: item.id)
                            }
                        }
                    }
                    .padding(16)

                case .grid:
                    LazyVGrid(columns: columns, spacing: 8) {
                        ForEach(items) { item in
                            GalleryGridCell(item: item) {
                                toggleFavorite(id: item.id)
                            }
                        }
                    }
                    .padding(16)
                }
            }
            .navigationTitle("Galería")
            .toolbar {
                Button(action: {
                    viewMode = viewMode == .grid ? .list : .grid
                }) {
                    Image(systemName: viewMode == .grid ? "list.bullet" : "square.grid.2x2")
                }
            }
        }
    }

    func toggleFavorite(id: Int) {
        if let index = items.firstIndex(where: { $0.id == id }) {
            items[index].isFavorite.toggle()
        }
    }
}

struct GalleryListRow: View {
    let item: GalleryItem
    let onFavoriteClick: () -> Void

    var body: some View {
        HStack(spacing: 16) {
            RoundedRectangle(cornerRadius: 8)
                .fill(item.color)
                .frame(width: 80, height: 80)

            Text(item.title)
                .font(.headline)

            Spacer()

            Button(action: onFavoriteClick) {
                Image(systemName: item.isFavorite ? "heart.fill" : "heart")
                    .foregroundColor(item.isFavorite ? .red : .gray)
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(8)
        .shadow(radius: 2)
    }
}

struct GalleryGridCell: View {
    let item: GalleryItem
    let onFavoriteClick: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            ZStack(alignment: .topTrailing) {
                Rectangle()
                    .fill(item.color)
                    .aspectRatio(1, contentMode: .fit)

                Button(action: onFavoriteClick) {
                    Image(systemName: item.isFavorite ? "heart.fill" : "heart")
                        .foregroundColor(item.isFavorite ? .red : .white)
                        .padding(8)
                }
            }

            Text(item.title)
                .font(.subheadline)
                .padding(8)
        }
        .background(Color.white)
        .cornerRadius(8)
        .shadow(radius: 2)
    }
}

#Preview {
    GalleryApp()
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear una app de productos con vista de lista y grid.

### Requisitos

- ✅ Modelo de datos: `Product(id, name, price, image, inCart)`
- ✅ Lista de 20 productos
- ✅ Toggle entre vista Lista y Grid
- ✅ En lista: mostrar imagen, nombre, precio, botón "Agregar al carrito"
- ✅ En grid: mostrar imagen, nombre, precio, ícono de carrito
- ✅ Estado para productos en carrito
- ✅ Contador de items en carrito en el TopBar

### Bonus

- Filtrar por categorías
- Buscar productos
- Ordenar por precio
- Pull-to-refresh

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **Lists**: [developer.android.com/jetpack/compose/lists](https://developer.android.com/jetpack/compose/lists)
- **LazyColumn**: [developer.android.com/reference/kotlin/androidx/compose/foundation/lazy/package-summary#LazyColumn](https://developer.android.com/reference/kotlin/androidx/compose/foundation/lazy/package-summary)
- **LazyVerticalGrid**: [developer.android.com/jetpack/compose/layouts/lazy#lazy-grids](https://developer.android.com/jetpack/compose/layouts/lazy#lazy-grids)

### SwiftUI
- **Lists**: [developer.apple.com/documentation/swiftui/list](https://developer.apple.com/documentation/swiftui/list)
- **Lazy Grids**: [developer.apple.com/documentation/swiftui/lazyvgrid](https://developer.apple.com/documentation/swiftui/lazyvgrid)
- **ScrollView**: [developer.apple.com/documentation/swiftui/scrollview](https://developer.apple.com/documentation/swiftui/scrollview)

---

**Anterior:** [04_LAYOUTS_BASICOS.md](04_LAYOUTS_BASICOS.md)
**Siguiente:** [06_NAVEGACION.md](06_NAVEGACION.md) - Navegación entre pantallas

