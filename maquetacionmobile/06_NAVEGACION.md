# 🧭 Navegación

> **Jetpack Compose (Android) & SwiftUI (iOS) - Navegación entre Pantallas**

---

## 🎯 Objetivo

Dominar la navegación entre pantallas, pasar datos entre vistas, y crear flujos de navegación complejos.

---

## 📚 Conceptos Fundamentales

### Patrones de Navegación Móvil

| Patrón | Descripción | Uso |
|--------|-------------|-----|
| **Stack Navigation** | Apilar pantallas (push/pop) | Flujo lineal (detalles, wizard) |
| **Tab Navigation** | Pestañas en bottom/top | Secciones principales de la app |
| **Drawer Navigation** | Menú lateral deslizable | Navegación secundaria |
| **Modal** | Pantalla temporal sobre la actual | Acciones rápidas, formularios |

---

## 📱 Stack Navigation - Navegación Básica

### Jetpack Compose - Navigation Component

#### Setup

Primero añade la dependencia en `build.gradle.kts`:

```kotlin
dependencies {
    implementation("androidx.navigation:navigation-compose:2.7.7")
}
```

#### Navegación Básica

```kotlin
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "home"  // Pantalla inicial
    ) {
        // Definir rutas
        composable("home") {
            HomeScreen(
                onNavigateToDetails = {
                    navController.navigate("details")
                }
            )
        }

        composable("details") {
            DetailsScreen(
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}

@Composable
fun HomeScreen(onNavigateToDetails: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Home Screen", style = MaterialTheme.typography.headlineMedium)

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = onNavigateToDetails) {
            Text("Go to Details")
        }
    }
}

@Composable
fun DetailsScreen(onNavigateBack: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Details Screen", style = MaterialTheme.typography.headlineMedium)

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = onNavigateBack) {
            Text("Go Back")
        }
    }
}
```

#### Pasar Argumentos (String/Int)

```kotlin
@Composable
fun AppNavigationWithArgs() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "users") {
        composable("users") {
            UsersListScreen(
                onUserClick = { userId ->
                    navController.navigate("user/$userId")
                }
            )
        }

        composable(
            route = "user/{userId}",
            arguments = listOf(navArgument("userId") { type = NavType.IntType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getInt("userId") ?: 0
            UserDetailScreen(userId = userId)
        }
    }
}

@Composable
fun UsersListScreen(onUserClick: (Int) -> Unit) {
    val users = remember { (1..10).map { "Usuario $it" } }

    LazyColumn {
        items(users.size) { index ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp)
                    .clickable { onUserClick(index + 1) }
            ) {
                Text(
                    text = users[index],
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }
    }
}

@Composable
fun UserDetailScreen(userId: Int) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Detalles del Usuario #$userId",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text("Nombre: Usuario $userId")
        Text("Email: usuario$userId@example.com")
        Text("Teléfono: +1 234 567 ${userId}000")
    }
}
```

#### Pasar Objetos Complejos

Para objetos complejos, usa un ViewModel compartido o serializa a JSON:

```kotlin
// Opción 1: ViewModel compartido (recomendado)
@Composable
fun AppWithSharedViewModel() {
    val navController = rememberNavController()
    val viewModel: SharedViewModel = viewModel()

    NavHost(navController = navController, startDestination = "list") {
        composable("list") {
            ProductListScreen(
                viewModel = viewModel,
                onProductClick = { product ->
                    viewModel.selectProduct(product)
                    navController.navigate("details")
                }
            )
        }

        composable("details") {
            ProductDetailScreen(viewModel = viewModel)
        }
    }
}

class SharedViewModel : ViewModel() {
    private val _selectedProduct = MutableLiveData<Product>()
    val selectedProduct: LiveData<Product> = _selectedProduct

    fun selectProduct(product: Product) {
        _selectedProduct.value = product
    }
}

// Opción 2: Serializar a JSON (para objetos simples)
@Composable
fun AppWithJsonArgs() {
    val navController = rememberNavController()
    val gson = Gson()

    NavHost(navController = navController, startDestination = "list") {
        composable("list") {
            ProductListScreen { product ->
                val productJson = Uri.encode(gson.toJson(product))
                navController.navigate("details/$productJson")
            }
        }

        composable(
            route = "details/{productJson}",
            arguments = listOf(navArgument("productJson") { type = NavType.StringType })
        ) { backStackEntry ->
            val productJson = backStackEntry.arguments?.getString("productJson")
            val product = gson.fromJson(productJson, Product::class.java)
            ProductDetailScreen(product = product)
        }
    }
}
```

---

### SwiftUI - NavigationStack

#### Navegación Básica (iOS 16+)

```swift
struct AppNavigation: View {
    var body: some View {
        NavigationStack {
            HomeScreen()
        }
    }
}

struct HomeScreen: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("Home Screen")
                .font(.largeTitle)

            NavigationLink("Go to Details") {
                DetailsScreen()
            }
            .buttonStyle(.borderedProminent)
        }
        .navigationTitle("Home")
    }
}

struct DetailsScreen: View {
    @Environment(\.dismiss) var dismiss

    var body: some View {
        VStack(spacing: 16) {
            Text("Details Screen")
                .font(.largeTitle)

            Button("Go Back") {
                dismiss()
            }
            .buttonStyle(.bordered)
        }
        .navigationTitle("Details")
    }
}
```

#### Pasar Argumentos

```swift
struct UsersListScreen: View {
    let users = (1...10).map { "Usuario \($0)" }

    var body: some View {
        NavigationStack {
            List(1...10, id: \.self) { userId in
                NavigationLink(value: userId) {
                    Text("Usuario \(userId)")
                        .font(.headline)
                }
            }
            .navigationDestination(for: Int.self) { userId in
                UserDetailScreen(userId: userId)
            }
            .navigationTitle("Usuarios")
        }
    }
}

struct UserDetailScreen: View {
    let userId: Int

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Detalles del Usuario #\(userId)")
                .font(.title)
                .fontWeight(.bold)

            Divider()

            Text("Nombre: Usuario \(userId)")
            Text("Email: usuario\(userId)@example.com")
            Text("Teléfono: +1 234 567 \(userId)000")

            Spacer()
        }
        .padding()
        .navigationTitle("Usuario #\(userId)")
    }
}
```

#### Pasar Objetos Complejos

```swift
struct Product: Identifiable, Hashable {
    let id: Int
    let name: String
    let price: Double
}

struct ProductListScreen: View {
    let products = [
        Product(id: 1, name: "MacBook Pro", price: 1999),
        Product(id: 2, name: "iPhone 15", price: 999),
        Product(id: 3, name: "AirPods Pro", price: 249)
    ]

    var body: some View {
        NavigationStack {
            List(products) { product in
                NavigationLink(value: product) {
                    HStack {
                        Text(product.name)
                        Spacer()
                        Text("$\(Int(product.price))")
                            .foregroundColor(.secondary)
                    }
                }
            }
            .navigationDestination(for: Product.self) { product in
                ProductDetailScreen(product: product)
            }
            .navigationTitle("Productos")
        }
    }
}

struct ProductDetailScreen: View {
    let product: Product

    var body: some View {
        VStack(spacing: 20) {
            Text(product.name)
                .font(.largeTitle)
                .fontWeight(.bold)

            Text("$\(Int(product.price))")
                .font(.title)
                .foregroundColor(.green)

            Button("Agregar al Carrito") {
                // Acción
            }
            .buttonStyle(.borderedProminent)

            Spacer()
        }
        .padding()
        .navigationTitle("Detalles")
    }
}
```

#### Navegación Programática

```swift
struct ProgrammaticNavigation: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 16) {
                Button("Go to Screen 1") {
                    path.append(1)
                }

                Button("Go to Screen 2") {
                    path.append(2)
                }

                Button("Go to Screen 3") {
                    path.append(3)
                }

                Button("Go to Root") {
                    path = NavigationPath()  // Vuelve al inicio
                }
            }
            .navigationDestination(for: Int.self) { screen in
                ScreenView(screenNumber: screen, path: $path)
            }
            .navigationTitle("Home")
        }
    }
}

struct ScreenView: View {
    let screenNumber: Int
    @Binding var path: NavigationPath

    var body: some View {
        VStack(spacing: 16) {
            Text("Screen \(screenNumber)")
                .font(.largeTitle)

            Button("Go to Next") {
                path.append(screenNumber + 1)
            }

            Button("Back to Root") {
                path = NavigationPath()
            }
        }
        .navigationTitle("Screen \(screenNumber)")
    }
}
```

---

### Comparación Stack Navigation

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Setup | `NavHost + NavController` | `NavigationStack` |
| Navegar adelante | `navController.navigate("route")` | `NavigationLink` o `path.append()` |
| Navegar atrás | `navController.popBackStack()` | `dismiss()` |
| Pasar args simples | Route params: `"user/{id}"` | `navigationDestination(for: Int.self)` |
| Pasar objetos | ViewModel o JSON serializado | Directamente si es `Hashable` |
| Navegación programática | `navController.navigate()` | `NavigationPath` binding |

---

## 📑 Tab Navigation - Pestañas

### Jetpack Compose - BottomNavigation

```kotlin
@Composable
fun TabNavigationApp() {
    val navController = rememberNavController()
    val items = listOf(
        BottomNavItem("home", "Home", Icons.Default.Home),
        BottomNavItem("search", "Search", Icons.Default.Search),
        BottomNavItem("profile", "Profile", Icons.Default.Person)
    )

    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route

                items.forEach { item ->
                    NavigationBarItem(
                        icon = { Icon(item.icon, contentDescription = item.label) },
                        label = { Text(item.label) },
                        selected = currentRoute == item.route,
                        onClick = {
                            navController.navigate(item.route) {
                                // Evitar múltiples copias en el stack
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(paddingValues)
        ) {
            composable("home") { HomeTabScreen() }
            composable("search") { SearchTabScreen() }
            composable("profile") { ProfileTabScreen() }
        }
    }
}

data class BottomNavItem(
    val route: String,
    val label: String,
    val icon: ImageVector
)

@Composable
fun HomeTabScreen() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("Home Tab", style = MaterialTheme.typography.headlineMedium)
    }
}

@Composable
fun SearchTabScreen() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("Search Tab", style = MaterialTheme.typography.headlineMedium)
    }
}

@Composable
fun ProfileTabScreen() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("Profile Tab", style = MaterialTheme.typography.headlineMedium)
    }
}
```

---

### SwiftUI - TabView

```swift
struct TabNavigationApp: View {
    var body: some View {
        TabView {
            HomeTabScreen()
                .tabItem {
                    Label("Home", systemImage: "house")
                }

            SearchTabScreen()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }

            ProfileTabScreen()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
    }
}

struct HomeTabScreen: View {
    var body: some View {
        NavigationStack {
            Text("Home Tab")
                .font(.largeTitle)
                .navigationTitle("Home")
        }
    }
}

struct SearchTabScreen: View {
    var body: some View {
        NavigationStack {
            Text("Search Tab")
                .font(.largeTitle)
                .navigationTitle("Search")
        }
    }
}

struct ProfileTabScreen: View {
    var body: some View {
        NavigationStack {
            Text("Profile Tab")
                .font(.largeTitle)
                .navigationTitle("Profile")
        }
    }
}
```

#### TabView con Badge

```swift
struct TabViewWithBadge: View {
    @State private var notificationCount = 5

    var body: some View {
        TabView {
            Text("Home")
                .tabItem {
                    Label("Home", systemImage: "house")
                }

            Text("Messages")
                .tabItem {
                    Label("Messages", systemImage: "message")
                }
                .badge(notificationCount)  // iOS 15+

            Text("Profile")
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
    }
}
```

---

## 🎨 Ejemplo Completo: App de E-commerce

### Jetpack Compose

```kotlin
// Modelo de datos
data class Product(
    val id: Int,
    val name: String,
    val price: Double,
    val description: String,
    val category: String
)

// Main App
@Composable
fun EcommerceApp() {
    val navController = rememberNavController()

    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route

                NavigationBarItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                    label = { Text("Home") },
                    selected = currentRoute == "home",
                    onClick = { navController.navigate("home") }
                )

                NavigationBarItem(
                    icon = { Icon(Icons.Default.ShoppingCart, contentDescription = "Cart") },
                    label = { Text("Cart") },
                    selected = currentRoute == "cart",
                    onClick = { navController.navigate("cart") }
                )

                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                    label = { Text("Profile") },
                    selected = currentRoute == "profile",
                    onClick = { navController.navigate("profile") }
                )
            }
        }
    ) { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(paddingValues)
        ) {
            composable("home") {
                ProductListScreen(
                    onProductClick = { productId ->
                        navController.navigate("product/$productId")
                    }
                )
            }

            composable(
                route = "product/{productId}",
                arguments = listOf(navArgument("productId") { type = NavType.IntType })
            ) { backStackEntry ->
                val productId = backStackEntry.arguments?.getInt("productId") ?: 0
                ProductDetailScreen(
                    productId = productId,
                    onNavigateBack = { navController.popBackStack() }
                )
            }

            composable("cart") {
                CartScreen()
            }

            composable("profile") {
                ProfileScreen()
            }
        }
    }
}

@Composable
fun ProductListScreen(onProductClick: (Int) -> Unit) {
    val products = remember {
        listOf(
            Product(1, "MacBook Pro", 1999.0, "Laptop potente", "Tech"),
            Product(2, "iPhone 15", 999.0, "Smartphone", "Tech"),
            Product(3, "AirPods Pro", 249.0, "Audífonos", "Audio"),
            Product(4, "iPad Air", 599.0, "Tablet", "Tech"),
            Product(5, "Apple Watch", 399.0, "Smartwatch", "Wearables")
        )
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Text(
            text = "Productos",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(16.dp)
        )

        LazyColumn(
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(products) { product ->
                ProductCard(
                    product = product,
                    onClick = { onProductClick(product.id) }
                )
            }
        }
    }
}

@Composable
fun ProductCard(product: Product, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .background(Color.Gray.copy(alpha = 0.3f), shape = RoundedCornerShape(8.dp))
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = product.category,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "$${product.price}",
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.Green,
                    fontWeight = FontWeight.Bold
                )
            }

            Icon(
                imageVector = Icons.Default.ChevronRight,
                contentDescription = "Ver detalles",
                tint = Color.Gray
            )
        }
    }
}

@Composable
fun ProductDetailScreen(productId: Int, onNavigateBack: () -> Unit) {
    val product = remember {
        // En una app real, esto vendría de un ViewModel o repository
        Product(productId, "Producto $productId", 999.0, "Descripción del producto", "Tech")
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Top bar personalizado
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onNavigateBack) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Volver")
            }
            Text(
                text = "Detalles",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
        }

        Column(modifier = Modifier.padding(16.dp)) {
            // Imagen del producto
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(250.dp)
                    .background(Color.Gray.copy(alpha = 0.3f), shape = RoundedCornerShape(12.dp))
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = product.name,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )

            Text(
                text = product.category,
                style = MaterialTheme.typography.bodyMedium,
                color = Color.Gray
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "$${product.price}",
                style = MaterialTheme.typography.headlineLarge,
                color = Color.Green,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "Descripción",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )

            Text(
                text = product.description,
                style = MaterialTheme.typography.bodyMedium,
                color = Color.Gray
            )

            Spacer(modifier = Modifier.weight(1f))

            Button(
                onClick = { /* Agregar al carrito */ },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp)
            ) {
                Icon(Icons.Default.ShoppingCart, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Agregar al Carrito")
            }
        }
    }
}

@Composable
fun CartScreen() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("Carrito de Compras", style = MaterialTheme.typography.headlineMedium)
    }
}

@Preview(showBackground = true)
@Composable
fun EcommerceAppPreview() {
    EcommerceApp()
}
```

---

### SwiftUI

```swift
// Modelo de datos
struct Product: Identifiable, Hashable {
    let id: Int
    let name: String
    let price: Double
    let description: String
    let category: String
}

// Main App
struct EcommerceApp: View {
    var body: some View {
        TabView {
            ProductListScreen()
                .tabItem {
                    Label("Home", systemImage: "house")
                }

            CartScreen()
                .tabItem {
                    Label("Cart", systemImage: "cart")
                }

            ProfileScreen()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
    }
}

struct ProductListScreen: View {
    let products = [
        Product(id: 1, name: "MacBook Pro", price: 1999, description: "Laptop potente", category: "Tech"),
        Product(id: 2, name: "iPhone 15", price: 999, description: "Smartphone", category: "Tech"),
        Product(id: 3, name: "AirPods Pro", price: 249, description: "Audífonos", category: "Audio"),
        Product(id: 4, name: "iPad Air", price: 599, description: "Tablet", category: "Tech"),
        Product(id: 5, name: "Apple Watch", price: 399, description: "Smartwatch", category: "Wearables")
    ]

    var body: some View {
        NavigationStack {
            List(products) { product in
                NavigationLink(value: product) {
                    ProductRow(product: product)
                }
            }
            .navigationDestination(for: Product.self) { product in
                ProductDetailScreen(product: product)
            }
            .navigationTitle("Productos")
        }
    }
}

struct ProductRow: View {
    let product: Product

    var body: some View {
        HStack(spacing: 16) {
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.gray.opacity(0.3))
                .frame(width: 80, height: 80)

            VStack(alignment: .leading, spacing: 4) {
                Text(product.name)
                    .font(.headline)
                    .fontWeight(.bold)

                Text(product.category)
                    .font(.subheadline)
                    .foregroundColor(.gray)

                Text("$\(Int(product.price))")
                    .font(.headline)
                    .foregroundColor(.green)
                    .fontWeight(.bold)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .foregroundColor(.gray)
        }
        .padding(.vertical, 4)
    }
}

struct ProductDetailScreen: View {
    let product: Product
    @Environment(\.dismiss) var dismiss

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Imagen del producto
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.gray.opacity(0.3))
                    .frame(height: 250)

                VStack(alignment: .leading, spacing: 8) {
                    Text(product.name)
                        .font(.largeTitle)
                        .fontWeight(.bold)

                    Text(product.category)
                        .font(.subheadline)
                        .foregroundColor(.gray)

                    Text("$\(Int(product.price))")
                        .font(.title)
                        .foregroundColor(.green)
                        .fontWeight(.bold)

                    Divider()
                        .padding(.vertical, 8)

                    Text("Descripción")
                        .font(.headline)

                    Text(product.description)
                        .foregroundColor(.gray)
                }
                .padding(.horizontal)

                Spacer(minLength: 20)

                Button(action: {
                    // Agregar al carrito
                }) {
                    HStack {
                        Image(systemName: "cart")
                        Text("Agregar al Carrito")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal)
            }
        }
        .navigationTitle("Detalles")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct CartScreen: View {
    var body: some View {
        NavigationStack {
            Text("Carrito de Compras")
                .font(.largeTitle)
                .navigationTitle("Cart")
        }
    }
}

struct ProfileScreen: View {
    var body: some View {
        NavigationStack {
            Text("Perfil")
                .font(.largeTitle)
                .navigationTitle("Profile")
        }
    }
}

#Preview {
    EcommerceApp()
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear una app de noticias con navegación completa.

### Requisitos

**3 tabs:**
- Home: Lista de noticias
- Favorites: Noticias guardadas
- Profile: Perfil del usuario

**Navegación:**
- Al hacer click en una noticia → abrir pantalla de detalle
- En detalle: botón para marcar como favorito
- Botón de compartir

**Datos:**
- Crear modelo `News(id, title, summary, content, category, isFavorite)`
- Lista de 10 noticias dummy

### Bonus

- Filtrar noticias por categoría
- Búsqueda de noticias
- Pull-to-refresh
- Persistir favoritos (próxima guía)

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **Navigation**: [developer.android.com/jetpack/compose/navigation](https://developer.android.com/jetpack/compose/navigation)
- **BottomNavigation**: [developer.android.com/reference/kotlin/androidx/compose/material3/package-summary#NavigationBar](https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary)

### SwiftUI
- **NavigationStack**: [developer.apple.com/documentation/swiftui/navigationstack](https://developer.apple.com/documentation/swiftui/navigationstack)
- **TabView**: [developer.apple.com/documentation/swiftui/tabview](https://developer.apple.com/documentation/swiftui/tabview)

---

**Anterior:** [05_LISTAS_Y_GRIDS.md](05_LISTAS_Y_GRIDS.md)
**Siguiente:** [07_STATE_MANAGEMENT.md](07_STATE_MANAGEMENT.md) - Gestión de Estado

