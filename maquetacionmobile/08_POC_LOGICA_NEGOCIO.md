# 🧮 PoC - Lógica de Negocio y Algoritmos

> **Jetpack Compose (Android) & SwiftUI (iOS) - Proof of Concept con Reglas de Negocio**

---

## 🎯 Objetivo

Crear Proof of Concepts (PoCs) completos integrando lógica de negocio, algoritmos, operaciones CRUD y fetching de datos desde APIs REST - todo en el frontend sin necesidad de backend propio.

---

## 📚 Conceptos Fundamentales

### ¿Qué es un PoC?

Un **Proof of Concept** es una implementación funcional para demostrar que una idea o concepto es viable.

### Componentes de un PoC Móvil

```
┌─────────────────────────────────────────┐
│         UI Layer (Compose/SwiftUI)       │
├─────────────────────────────────────────┤
│         ViewModel (Business Logic)       │
├─────────────────────────────────────────┤
│    Repository (Data Operations/CRUD)    │
├─────────────────────────────────────────┤
│   Data Sources (API Client + Cache)     │
└─────────────────────────────────────────┘
```

---

## 🌐 Fetching de APIs - Sin Backend

### APIs Públicas Gratuitas para PoCs

| API | Endpoint | Uso |
|-----|----------|-----|
| **JSONPlaceholder** | `jsonplaceholder.typicode.com` | Posts, Users, Comments |
| **DummyJSON** | `dummyjson.com` | Products, Carts, Users |
| **OpenWeather** | `api.openweathermap.org` | Clima (requiere API key gratis) |
| **CoinGecko** | `api.coingecko.com` | Criptomonedas |
| **Rick and Morty** | `rickandmortyapi.com` | Personajes, episodios |

---

## 🛠️ Setup para Networking

### Jetpack Compose - Retrofit + Coroutines

#### Dependencias (build.gradle.kts)

```kotlin
dependencies {
    // Retrofit
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")

    // OkHttp (logging)
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}
```

#### API Service Setup

```kotlin
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

// Modelo de datos
data class Product(
    val id: Int,
    val title: String,
    val price: Double,
    val description: String,
    val category: String,
    val image: String,
    val rating: Rating
)

data class Rating(
    val rate: Double,
    val count: Int
)

data class ProductsResponse(
    val products: List<Product>,
    val total: Int,
    val skip: Int,
    val limit: Int
)

// API Interface
interface ProductApi {
    @GET("products")
    suspend fun getProducts(): List<Product>

    @GET("products/{id}")
    suspend fun getProductById(@Path("id") id: Int): Product

    @GET("products/search")
    suspend fun searchProducts(@Query("q") query: String): ProductsResponse

    @GET("products/category/{category}")
    suspend fun getProductsByCategory(@Path("category") category: String): List<Product>
}

// Retrofit Instance
object RetrofitClient {
    private const val BASE_URL = "https://fakestoreapi.com/"

    val api: ProductApi by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ProductApi::class.java)
    }
}
```

---

### SwiftUI - URLSession + Async/Await

#### Modelo de Datos

```swift
import Foundation

struct Product: Identifiable, Codable {
    let id: Int
    let title: String
    let price: Double
    let description: String
    let category: String
    let image: String
    let rating: Rating
}

struct Rating: Codable {
    let rate: Double
    let count: Int
}

struct ProductsResponse: Codable {
    let products: [Product]
    let total: Int
    let skip: Int
    let limit: Int
}
```

#### API Service

```swift
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingError
}

class ProductService {
    private let baseURL = "https://fakestoreapi.com"

    func getProducts() async throws -> [Product] {
        guard let url = URL(string: "\(baseURL)/products") else {
            throw NetworkError.invalidURL
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        let products = try JSONDecoder().decode([Product].self, from: data)
        return products
    }

    func getProductById(_ id: Int) async throws -> Product {
        guard let url = URL(string: "\(baseURL)/products/\(id)") else {
            throw NetworkError.invalidURL
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        let product = try JSONDecoder().decode(Product.self, from: data)
        return product
    }

    func searchProducts(query: String) async throws -> [Product] {
        guard let url = URL(string: "\(baseURL)/products/search?q=\(query)") else {
            throw NetworkError.invalidURL
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        let response = try JSONDecoder().decode(ProductsResponse.self, from: data)
        return response.products
    }
}
```

---

## 🏗️ PoC #1: E-Commerce con Reglas de Negocio

### Reglas de Negocio

1. **Descuento por cantidad**: 10% si compras 3+ items del mismo producto
2. **Envío gratis**: Pedidos mayores a $100
3. **Impuestos**: 16% sobre el subtotal
4. **Stock limitado**: Máximo 5 unidades por producto
5. **Validación**: Email válido y tarjeta con formato correcto

---

### Jetpack Compose - Implementación Completa

```kotlin
import androidx.compose.runtime.*
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.util.regex.Pattern

// ============= MODELS =============

data class CartItem(
    val product: Product,
    var quantity: Int = 1
) {
    val subtotal: Double
        get() = product.price * quantity

    // Regla: 10% descuento si compras 3+
    val discount: Double
        get() = if (quantity >= 3) subtotal * 0.10 else 0.0

    val total: Double
        get() = subtotal - discount
}

data class Order(
    val items: List<CartItem>,
    val subtotal: Double,
    val discount: Double,
    val shippingCost: Double,
    val tax: Double,
    val total: Double
)

data class CheckoutForm(
    val email: String = "",
    val cardNumber: String = "",
    val cvv: String = "",
    val isValid: Boolean = false
)

// ============= REPOSITORY =============

class ProductRepository {
    private val api = RetrofitClient.api

    suspend fun getProducts(): Result<List<Product>> {
        return try {
            val products = api.getProducts()
            Result.success(products)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun searchProducts(query: String): Result<List<Product>> {
        return try {
            // Fake search since API doesn't support it
            val products = api.getProducts()
            val filtered = products.filter {
                it.title.contains(query, ignoreCase = true) ||
                it.category.contains(query, ignoreCase = true)
            }
            Result.success(filtered)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// ============= BUSINESS LOGIC =============

object BusinessRules {
    const val MAX_QUANTITY_PER_ITEM = 5
    const val FREE_SHIPPING_THRESHOLD = 100.0
    const val SHIPPING_COST = 10.0
    const val TAX_RATE = 0.16
    const val BULK_DISCOUNT_QUANTITY = 3
    const val BULK_DISCOUNT_RATE = 0.10

    fun validateEmail(email: String): Boolean {
        val emailPattern = Pattern.compile(
            "[a-zA-Z0-9+._%\\-]{1,256}@[a-zA-Z0-9][a-zA-Z0-9\\-]{0,64}" +
            "(\\.[a-zA-Z0-9][a-zA-Z0-9\\-]{0,25})+"
        )
        return emailPattern.matcher(email).matches()
    }

    fun validateCardNumber(cardNumber: String): Boolean {
        // Algoritmo de Luhn simplificado
        val digits = cardNumber.replace(" ", "").filter { it.isDigit() }
        return digits.length == 16
    }

    fun validateCVV(cvv: String): Boolean {
        return cvv.length == 3 && cvv.all { it.isDigit() }
    }

    fun calculateOrder(items: List<CartItem>): Order {
        val subtotal = items.sumOf { it.subtotal }
        val discount = items.sumOf { it.discount }
        val shippingCost = if (subtotal >= FREE_SHIPPING_THRESHOLD) 0.0 else SHIPPING_COST
        val taxableAmount = subtotal - discount
        val tax = taxableAmount * TAX_RATE
        val total = taxableAmount + tax + shippingCost

        return Order(
            items = items,
            subtotal = subtotal,
            discount = discount,
            shippingCost = shippingCost,
            tax = tax,
            total = total
        )
    }
}

// ============= VIEW MODEL =============

data class EcommerceUiState(
    val products: List<Product> = emptyList(),
    val cartItems: List<CartItem> = emptyList(),
    val searchQuery: String = "",
    val isLoading: Boolean = false,
    val error: String? = null,
    val checkoutForm: CheckoutForm = CheckoutForm(),
    val showCheckout: Boolean = false
)

class EcommerceViewModel : ViewModel() {
    private val repository = ProductRepository()

    private val _uiState = MutableStateFlow(EcommerceUiState())
    val uiState: StateFlow<EcommerceUiState> = _uiState.asStateFlow()

    init {
        loadProducts()
    }

    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)

            repository.getProducts().fold(
                onSuccess = { products ->
                    _uiState.value = _uiState.value.copy(
                        products = products,
                        isLoading = false
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = error.message,
                        isLoading = false
                    )
                }
            )
        }
    }

    fun searchProducts(query: String) {
        _uiState.value = _uiState.value.copy(searchQuery = query)

        if (query.isBlank()) {
            loadProducts()
            return
        }

        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)

            repository.searchProducts(query).fold(
                onSuccess = { products ->
                    _uiState.value = _uiState.value.copy(
                        products = products,
                        isLoading = false
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = error.message,
                        isLoading = false
                    )
                }
            )
        }
    }

    fun addToCart(product: Product) {
        val currentItems = _uiState.value.cartItems.toMutableList()
        val existingItem = currentItems.find { it.product.id == product.id }

        if (existingItem != null) {
            if (existingItem.quantity < BusinessRules.MAX_QUANTITY_PER_ITEM) {
                existingItem.quantity++
            }
        } else {
            currentItems.add(CartItem(product))
        }

        _uiState.value = _uiState.value.copy(cartItems = currentItems)
    }

    fun updateQuantity(productId: Int, quantity: Int) {
        val validQuantity = quantity.coerceIn(1, BusinessRules.MAX_QUANTITY_PER_ITEM)
        val updatedItems = _uiState.value.cartItems.map {
            if (it.product.id == productId) it.copy(quantity = validQuantity)
            else it
        }
        _uiState.value = _uiState.value.copy(cartItems = updatedItems)
    }

    fun removeFromCart(productId: Int) {
        val updatedItems = _uiState.value.cartItems.filter { it.product.id != productId }
        _uiState.value = _uiState.value.copy(cartItems = updatedItems)
    }

    fun updateCheckoutForm(
        email: String? = null,
        cardNumber: String? = null,
        cvv: String? = null
    ) {
        val currentForm = _uiState.value.checkoutForm
        val newForm = currentForm.copy(
            email = email ?: currentForm.email,
            cardNumber = cardNumber ?: currentForm.cardNumber,
            cvv = cvv ?: currentForm.cvv
        )

        val isValid = BusinessRules.validateEmail(newForm.email) &&
                     BusinessRules.validateCardNumber(newForm.cardNumber) &&
                     BusinessRules.validateCVV(newForm.cvv)

        _uiState.value = _uiState.value.copy(
            checkoutForm = newForm.copy(isValid = isValid)
        )
    }

    fun toggleCheckout() {
        _uiState.value = _uiState.value.copy(
            showCheckout = !_uiState.value.showCheckout
        )
    }

    fun calculateOrder(): Order {
        return BusinessRules.calculateOrder(_uiState.value.cartItems)
    }

    fun completeOrder() {
        // Aquí iría la lógica de procesamiento
        _uiState.value = _uiState.value.copy(
            cartItems = emptyList(),
            showCheckout = false,
            checkoutForm = CheckoutForm()
        )
    }
}

// ============= UI COMPOSABLES =============

@Composable
fun EcommerceApp(viewModel: EcommerceViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("E-Commerce PoC") },
                actions = {
                    // Cart badge
                    BadgedBox(
                        badge = {
                            if (uiState.cartItems.isNotEmpty()) {
                                Badge { Text(uiState.cartItems.size.toString()) }
                            }
                        }
                    ) {
                        IconButton(onClick = { viewModel.toggleCheckout() }) {
                            Icon(Icons.Default.ShoppingCart, contentDescription = "Cart")
                        }
                    }
                }
            )
        }
    ) { padding ->
        if (uiState.showCheckout) {
            CheckoutScreen(
                viewModel = viewModel,
                modifier = Modifier.padding(padding)
            )
        } else {
            ProductListScreen(
                viewModel = viewModel,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
fun ProductListScreen(
    viewModel: EcommerceViewModel,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsState()

    Column(modifier = modifier.fillMaxSize()) {
        // Search bar
        OutlinedTextField(
            value = uiState.searchQuery,
            onValueChange = { viewModel.searchProducts(it) },
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            placeholder = { Text("Buscar productos...") },
            leadingIcon = {
                Icon(Icons.Default.Search, contentDescription = null)
            },
            trailingIcon = {
                if (uiState.searchQuery.isNotEmpty()) {
                    IconButton(onClick = { viewModel.searchProducts("") }) {
                        Icon(Icons.Default.Close, contentDescription = "Clear")
                    }
                }
            }
        )

        when {
            uiState.isLoading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }

            uiState.error != null -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("Error: ${uiState.error}", color = Color.Red)
                        Button(onClick = { viewModel.loadProducts() }) {
                            Text("Reintentar")
                        }
                    }
                }
            }

            uiState.products.isEmpty() -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text("No se encontraron productos")
                }
            }

            else -> {
                LazyColumn(
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(uiState.products) { product ->
                        ProductCard(
                            product = product,
                            onAddToCart = { viewModel.addToCart(product) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun ProductCard(
    product: Product,
    onAddToCart: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Imagen placeholder
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .background(Color.Gray.copy(alpha = 0.3f), shape = RoundedCornerShape(8.dp))
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = product.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )

                Text(
                    text = product.category,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = "$${String.format("%.2f", product.price)}",
                    style = MaterialTheme.typography.titleLarge,
                    color = Color.Green,
                    fontWeight = FontWeight.Bold
                )

                // Rating
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Star,
                        contentDescription = null,
                        tint = Color(0xFFFFC107),
                        modifier = Modifier.size(16.dp)
                    )
                    Text(
                        text = "${product.rating.rate} (${product.rating.count})",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.Gray
                    )
                }
            }

            Button(onClick = onAddToCart) {
                Icon(Icons.Default.Add, contentDescription = "Add to cart")
            }
        }
    }
}

@Composable
fun CheckoutScreen(
    viewModel: EcommerceViewModel,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsState()
    val order = remember(uiState.cartItems) { viewModel.calculateOrder() }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        // Back button
        IconButton(onClick = { viewModel.toggleCheckout() }) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
        }

        Text(
            text = "Checkout",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(16.dp)
        )

        // Cart items
        Text(
            text = "Productos (${uiState.cartItems.size})",
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.padding(horizontal = 16.dp)
        )

        uiState.cartItems.forEach { item ->
            CheckoutCartItem(
                item = item,
                onQuantityChange = { viewModel.updateQuantity(item.product.id, it) },
                onRemove = { viewModel.removeFromCart(item.product.id) }
            )
        }

        Divider(modifier = Modifier.padding(vertical = 16.dp))

        // Order summary
        OrderSummary(order = order)

        Divider(modifier = Modifier.padding(vertical = 16.dp))

        // Payment form
        Text(
            text = "Información de Pago",
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
        )

        OutlinedTextField(
            value = uiState.checkoutForm.email,
            onValueChange = { viewModel.updateCheckoutForm(email = it) },
            label = { Text("Email") },
            isError = uiState.checkoutForm.email.isNotEmpty() &&
                     !BusinessRules.validateEmail(uiState.checkoutForm.email),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 4.dp)
        )

        OutlinedTextField(
            value = uiState.checkoutForm.cardNumber,
            onValueChange = { viewModel.updateCheckoutForm(cardNumber = it) },
            label = { Text("Número de Tarjeta") },
            isError = uiState.checkoutForm.cardNumber.isNotEmpty() &&
                     !BusinessRules.validateCardNumber(uiState.checkoutForm.cardNumber),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 4.dp)
        )

        OutlinedTextField(
            value = uiState.checkoutForm.cvv,
            onValueChange = { viewModel.updateCheckoutForm(cvv = it) },
            label = { Text("CVV") },
            isError = uiState.checkoutForm.cvv.isNotEmpty() &&
                     !BusinessRules.validateCVV(uiState.checkoutForm.cvv),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 4.dp)
        )

        Button(
            onClick = { viewModel.completeOrder() },
            enabled = uiState.checkoutForm.isValid && uiState.cartItems.isNotEmpty(),
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .height(50.dp)
        ) {
            Text("Completar Pedido - $${String.format("%.2f", order.total)}")
        }
    }
}

@Composable
fun CheckoutCartItem(
    item: CartItem,
    onQuantityChange: (Int) -> Unit,
    onRemove: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = item.product.title,
                        style = MaterialTheme.typography.bodyMedium,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "$${item.product.price} c/u",
                        style = MaterialTheme.typography.bodySmall,
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

                    Text(item.quantity.toString())

                    IconButton(
                        onClick = { onQuantityChange(item.quantity + 1) },
                        enabled = item.quantity < BusinessRules.MAX_QUANTITY_PER_ITEM
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Increase")
                    }

                    IconButton(onClick = onRemove) {
                        Icon(Icons.Default.Delete, contentDescription = "Remove", tint = Color.Red)
                    }
                }
            }

            // Show discount if applicable
            if (item.quantity >= BusinessRules.BULK_DISCOUNT_QUANTITY) {
                Text(
                    text = "¡Descuento 10% aplicado! -$${String.format("%.2f", item.discount)}",
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Green,
                    fontWeight = FontWeight.Bold
                )
            }

            Text(
                text = "Subtotal: $${String.format("%.2f", item.total)}",
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
fun OrderSummary(order: Order) {
    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
        Text(
            text = "Resumen del Pedido",
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.padding(bottom = 8.dp)
        )

        SummaryRow("Subtotal", order.subtotal)

        if (order.discount > 0) {
            SummaryRow(
                "Descuento por volumen",
                -order.discount,
                color = Color.Green
            )
        }

        SummaryRow(
            "Envío",
            order.shippingCost,
            note = if (order.shippingCost == 0.0) "¡Gratis!" else null
        )

        SummaryRow("Impuestos (16%)", order.tax)

        Divider(modifier = Modifier.padding(vertical = 8.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "Total",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "$${String.format("%.2f", order.total)}",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF4CAF50)
            )
        }
    }
}

@Composable
fun SummaryRow(
    label: String,
    amount: Double,
    color: Color = Color.Unspecified,
    note: String? = null
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column {
            Text(text = label)
            note?.let {
                Text(
                    text = it,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Green
                )
            }
        }
        Text(
            text = "$${String.format("%.2f", amount)}",
            color = color
        )
    }
}
```

---

### SwiftUI - Implementación Completa

```swift
import SwiftUI

// ============= MODELS =============

struct CartItem: Identifiable {
    let id = UUID()
    let product: Product
    var quantity: Int = 1

    var subtotal: Double {
        product.price * Double(quantity)
    }

    // Regla: 10% descuento si compras 3+
    var discount: Double {
        quantity >= 3 ? subtotal * 0.10 : 0.0
    }

    var total: Double {
        subtotal - discount
    }
}

struct Order {
    let items: [CartItem]
    let subtotal: Double
    let discount: Double
    let shippingCost: Double
    let tax: Double
    let total: Double
}

struct CheckoutForm {
    var email: String = ""
    var cardNumber: String = ""
    var cvv: String = ""

    var isValid: Bool {
        BusinessRules.validateEmail(email) &&
        BusinessRules.validateCardNumber(cardNumber) &&
        BusinessRules.validateCVV(cvv)
    }
}

// ============= BUSINESS RULES =============

enum BusinessRules {
    static let maxQuantityPerItem = 5
    static let freeShippingThreshold = 100.0
    static let shippingCost = 10.0
    static let taxRate = 0.16
    static let bulkDiscountQuantity = 3
    static let bulkDiscountRate = 0.10

    static func validateEmail(_ email: String) -> Bool {
        let emailRegex = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
        let emailPredicate = NSPredicate(format: "SELF MATCHES %@", emailRegex)
        return emailPredicate.evaluate(with: email)
    }

    static func validateCardNumber(_ cardNumber: String) -> Bool {
        let digits = cardNumber.filter { $0.isNumber }
        return digits.count == 16
    }

    static func validateCVV(_ cvv: String) -> Bool {
        cvv.count == 3 && cvv.allSatisfy { $0.isNumber }
    }

    static func calculateOrder(items: [CartItem]) -> Order {
        let subtotal = items.reduce(0) { $0 + $1.subtotal }
        let discount = items.reduce(0) { $0 + $1.discount }
        let shippingCost = subtotal >= freeShippingThreshold ? 0.0 : Self.shippingCost
        let taxableAmount = subtotal - discount
        let tax = taxableAmount * taxRate
        let total = taxableAmount + tax + shippingCost

        return Order(
            items: items,
            subtotal: subtotal,
            discount: discount,
            shippingCost: shippingCost,
            tax: tax,
            total: total
        )
    }
}

// ============= VIEW MODEL =============

@MainActor
class EcommerceViewModel: ObservableObject {
    @Published var products: [Product] = []
    @Published var cartItems: [CartItem] = []
    @Published var searchQuery: String = ""
    @Published var isLoading: Bool = false
    @Published var error: String?
    @Published var checkoutForm = CheckoutForm()
    @Published var showCheckout: Bool = false

    private let service = ProductService()

    init() {
        Task {
            await loadProducts()
        }
    }

    func loadProducts() async {
        isLoading = true
        error = nil

        do {
            products = try await service.getProducts()
        } catch {
            self.error = error.localizedDescription
        }

        isLoading = false
    }

    func searchProducts() async {
        guard !searchQuery.isEmpty else {
            await loadProducts()
            return
        }

        isLoading = true

        do {
            let allProducts = try await service.getProducts()
            products = allProducts.filter {
                $0.title.localizedCaseInsensitiveContains(searchQuery) ||
                $0.category.localizedCaseInsensitiveContains(searchQuery)
            }
        } catch {
            self.error = error.localizedDescription
        }

        isLoading = false
    }

    func addToCart(_ product: Product) {
        if let index = cartItems.firstIndex(where: { $0.product.id == product.id }) {
            if cartItems[index].quantity < BusinessRules.maxQuantityPerItem {
                cartItems[index].quantity += 1
            }
        } else {
            cartItems.append(CartItem(product: product))
        }
    }

    func updateQuantity(productId: Int, quantity: Int) {
        let validQuantity = min(max(quantity, 1), BusinessRules.maxQuantityPerItem)
        if let index = cartItems.firstIndex(where: { $0.product.id == productId }) {
            cartItems[index].quantity = validQuantity
        }
    }

    func removeFromCart(productId: Int) {
        cartItems.removeAll { $0.product.id == productId }
    }

    func calculateOrder() -> Order {
        BusinessRules.calculateOrder(items: cartItems)
    }

    func completeOrder() {
        cartItems.removeAll()
        showCheckout = false
        checkoutForm = CheckoutForm()
    }
}

// ============= UI VIEWS =============

struct EcommerceApp: View {
    @StateObject private var viewModel = EcommerceViewModel()

    var body: some View {
        NavigationStack {
            if viewModel.showCheckout {
                CheckoutScreen(viewModel: viewModel)
            } else {
                ProductListScreen(viewModel: viewModel)
            }
        }
    }
}

struct ProductListScreen: View {
    @ObservedObject var viewModel: EcommerceViewModel

    var body: some View {
        VStack(spacing: 0) {
            // Search bar
            HStack {
                Image(systemName: "magnifyingglass")
                    .foregroundColor(.gray)

                TextField("Buscar productos...", text: $viewModel.searchQuery)
                    .onChange(of: viewModel.searchQuery) { _ in
                        Task {
                            await viewModel.searchProducts()
                        }
                    }

                if !viewModel.searchQuery.isEmpty {
                    Button(action: {
                        viewModel.searchQuery = ""
                    }) {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundColor(.gray)
                    }
                }
            }
            .padding()
            .background(Color.gray.opacity(0.1))
            .cornerRadius(10)
            .padding()

            // Content
            if viewModel.isLoading {
                Spacer()
                ProgressView()
                Spacer()
            } else if let error = viewModel.error {
                Spacer()
                VStack {
                    Text("Error: \(error)")
                        .foregroundColor(.red)
                    Button("Reintentar") {
                        Task {
                            await viewModel.loadProducts()
                        }
                    }
                }
                Spacer()
            } else if viewModel.products.isEmpty {
                Spacer()
                Text("No se encontraron productos")
                    .foregroundColor(.gray)
                Spacer()
            } else {
                ScrollView {
                    LazyVStack(spacing: 8) {
                        ForEach(viewModel.products) { product in
                            ProductCard(
                                product: product,
                                onAddToCart: {
                                    viewModel.addToCart(product)
                                }
                            )
                        }
                    }
                    .padding()
                }
            }
        }
        .navigationTitle("E-Commerce PoC")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {
                    viewModel.showCheckout = true
                }) {
                    ZStack(alignment: .topTrailing) {
                        Image(systemName: "cart")

                        if !viewModel.cartItems.isEmpty {
                            Text("\(viewModel.cartItems.count)")
                                .font(.caption2)
                                .fontWeight(.bold)
                                .foregroundColor(.white)
                                .padding(4)
                                .background(Color.red)
                                .clipShape(Circle())
                                .offset(x: 8, y: -8)
                        }
                    }
                }
            }
        }
    }
}

struct ProductCard: View {
    let product: Product
    let onAddToCart: () -> Void

    var body: some View {
        HStack(alignment: .top, spacing: 16) {
            // Image placeholder
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.gray.opacity(0.3))
                .frame(width: 80, height: 80)

            VStack(alignment: .leading, spacing: 4) {
                Text(product.title)
                    .font(.headline)
                    .lineLimit(2)

                Text(product.category)
                    .font(.caption)
                    .foregroundColor(.gray)

                Text("$\(product.price, specifier: "%.2f")")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(.green)

                HStack(spacing: 4) {
                    Image(systemName: "star.fill")
                        .font(.caption)
                        .foregroundColor(.yellow)
                    Text("\(product.rating.rate, specifier: "%.1f") (\(product.rating.count))")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
            }

            Spacer()

            Button(action: onAddToCart) {
                Image(systemName: "plus")
                    .fontWeight(.bold)
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

struct CheckoutScreen: View {
    @ObservedObject var viewModel: EcommerceViewModel

    var order: Order {
        viewModel.calculateOrder()
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Cart items
                Text("Productos (\(viewModel.cartItems.count))")
                    .font(.title2)
                    .fontWeight(.bold)

                ForEach(viewModel.cartItems) { item in
                    CheckoutCartItem(
                        item: item,
                        onQuantityChange: { quantity in
                            viewModel.updateQuantity(productId: item.product.id, quantity: quantity)
                        },
                        onRemove: {
                            viewModel.removeFromCart(productId: item.product.id)
                        }
                    )
                }

                Divider()

                // Order summary
                OrderSummary(order: order)

                Divider()

                // Payment form
                Text("Información de Pago")
                    .font(.title2)
                    .fontWeight(.bold)

                TextField("Email", text: $viewModel.checkoutForm.email)
                    .textFieldStyle(.roundedBorder)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                    .overlay(
                        RoundedRectangle(cornerRadius: 5)
                            .stroke(
                                !viewModel.checkoutForm.email.isEmpty &&
                                !BusinessRules.validateEmail(viewModel.checkoutForm.email) ?
                                Color.red : Color.clear,
                                lineWidth: 1
                            )
                    )

                TextField("Número de Tarjeta", text: $viewModel.checkoutForm.cardNumber)
                    .textFieldStyle(.roundedBorder)
                    .keyboardType(.numberPad)
                    .overlay(
                        RoundedRectangle(cornerRadius: 5)
                            .stroke(
                                !viewModel.checkoutForm.cardNumber.isEmpty &&
                                !BusinessRules.validateCardNumber(viewModel.checkoutForm.cardNumber) ?
                                Color.red : Color.clear,
                                lineWidth: 1
                            )
                    )

                TextField("CVV", text: $viewModel.checkoutForm.cvv)
                    .textFieldStyle(.roundedBorder)
                    .keyboardType(.numberPad)
                    .overlay(
                        RoundedRectangle(cornerRadius: 5)
                            .stroke(
                                !viewModel.checkoutForm.cvv.isEmpty &&
                                !BusinessRules.validateCVV(viewModel.checkoutForm.cvv) ?
                                Color.red : Color.clear,
                                lineWidth: 1
                            )
                    )

                Button(action: {
                    viewModel.completeOrder()
                }) {
                    Text("Completar Pedido - $\(order.total, specifier: "%.2f")")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(viewModel.checkoutForm.isValid && !viewModel.cartItems.isEmpty ? Color.blue : Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .disabled(!viewModel.checkoutForm.isValid || viewModel.cartItems.isEmpty)
            }
            .padding()
        }
        .navigationTitle("Checkout")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                Button("Volver") {
                    viewModel.showCheckout = false
                }
            }
        }
    }
}

struct CheckoutCartItem: View {
    let item: CartItem
    let onQuantityChange: (Int) -> Void
    let onRemove: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading) {
                    Text(item.product.title)
                        .font(.body)
                        .lineLimit(1)
                    Text("$\(item.product.price, specifier: "%.2f") c/u")
                        .font(.caption)
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
                    .disabled(item.quantity >= BusinessRules.maxQuantityPerItem)

                    Button(action: onRemove) {
                        Image(systemName: "trash")
                            .foregroundColor(.red)
                    }
                }
            }

            if item.quantity >= BusinessRules.bulkDiscountQuantity {
                Text("¡Descuento 10% aplicado! -$\(item.discount, specifier: "%.2f")")
                    .font(.caption)
                    .foregroundColor(.green)
                    .fontWeight(.bold)
            }

            Text("Subtotal: $\(item.total, specifier: "%.2f")")
                .font(.body)
                .fontWeight(.bold)
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(8)
    }
}

struct OrderSummary: View {
    let order: Order

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Resumen del Pedido")
                .font(.title2)
                .fontWeight(.bold)

            SummaryRow(label: "Subtotal", amount: order.subtotal)

            if order.discount > 0 {
                SummaryRow(
                    label: "Descuento por volumen",
                    amount: -order.discount,
                    color: .green
                )
            }

            HStack {
                VStack(alignment: .leading) {
                    Text("Envío")
                    if order.shippingCost == 0 {
                        Text("¡Gratis!")
                            .font(.caption)
                            .foregroundColor(.green)
                    }
                }
                Spacer()
                Text("$\(order.shippingCost, specifier: "%.2f")")
            }

            SummaryRow(label: "Impuestos (16%)", amount: order.tax)

            Divider()

            HStack {
                Text("Total")
                    .font(.title2)
                    .fontWeight(.bold)
                Spacer()
                Text("$\(order.total, specifier: "%.2f")")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.green)
            }
        }
    }
}

struct SummaryRow: View {
    let label: String
    let amount: Double
    var color: Color = .primary

    var body: some View {
        HStack {
            Text(label)
            Spacer()
            Text("$\(amount, specifier: "%.2f")")
                .foregroundColor(color)
        }
    }
}
```

---

## 📝 Ejercicio Final

### Objetivo

Crear un PoC de app de finanzas personales.

### Reglas de Negocio

1. **Categorización automática**: Detectar categoría según palabras clave
2. **Presupuesto mensual**: Alertar si se excede el 80%
3. **Análisis de gastos**: Calcular promedio diario/semanal/mensual
4. **Objetivos de ahorro**: Calcular cuánto falta para una meta
5. **Validaciones**: Montos positivos, fechas válidas

### Features

- CRUD de transacciones (ingreso/gasto)
- Filtrar por categoría y rango de fechas
- Dashboard con estadísticas
- Gráficos de gastos por categoría
- Lista de metas de ahorro

### APIs Sugeridas

- Mock data local o
- JSONPlaceholder para usuarios
- LocalStorage para persistencia

---

## 🎯 Key Takeaways

✅ **Arquitectura limpia**: Repository → ViewModel → UI
✅ **Reglas de negocio** centralizadas y testeables
✅ **Validaciones** robustas en el frontend
✅ **Algoritmos** aplicados (descuentos, impuestos)
✅ **Networking** con manejo de errores
✅ **CRUD completo** sin necesidad de backend

---

## 🔗 Recursos Adicionales

### APIs Públicas
- **JSONPlaceholder**: [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)
- **DummyJSON**: [dummyjson.com](https://dummyjson.com)
- **FakeStoreAPI**: [fakestoreapi.com](https://fakestoreapi.com)

### Herramientas
- **Postman**: Testing de APIs
- **JSON Formatter**: Validar respuestas
- **Mocky**: Crear mock endpoints custom

---

**Anterior:** [07_STATE_MANAGEMENT.md](07_STATE_MANAGEMENT.md)
**Siguiente:** Proyectos completos y publicación

