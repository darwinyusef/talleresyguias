# 🎨 Temas y Dark Mode

> **Jetpack Compose (Android) & SwiftUI (iOS) - Personalización Visual**

---

## 🎯 Objetivo

Dominar la creación de temas personalizados, implementar dark mode, y gestionar la apariencia de la aplicación.

---

## 📚 Conceptos Fundamentales

### Sistema de Diseño

Un **sistema de diseño** define la identidad visual de tu app:

```
Sistema de Diseño
├── Colores (primarios, secundarios, backgrounds)
├── Tipografía (tamaños, weights, families)
├── Espaciado (margins, paddings)
├── Formas (border radius, shapes)
└── Elevación (shadows, depth)
```

### Material Design vs Human Interface Guidelines

| Aspecto | Material Design (Android) | HIG (iOS) |
|---------|--------------------------|-----------|
| **Filosofía** | Basado en papel y sombras | Plano con profundidad |
| **Colores** | Primary, Secondary, Tertiary | Accent colors + System colors |
| **Tipografía** | Roboto (default) | SF Pro (default) |
| **Componentes** | Material 3 | Native iOS components |

---

## 🎨 Colores y Paletas

### Jetpack Compose - Material Theme

#### Definir Paleta de Colores

```kotlin
import androidx.compose.material3.*
import androidx.compose.ui.graphics.Color

// Definir colores personalizados
val Purple40 = Color(0xFF6650a4)
val PurpleGrey40 = Color(0xFF625b71)
val Pink40 = Color(0xFF7D5260)

val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Pink80 = Color(0xFFEFB8C8)

// Paleta Light
private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    onPrimary = Color.White,
    primaryContainer = Purple80,
    onPrimaryContainer = Purple40,

    secondary = PurpleGrey40,
    onSecondary = Color.White,
    secondaryContainer = PurpleGrey80,
    onSecondaryContainer = PurpleGrey40,

    tertiary = Pink40,
    onTertiary = Color.White,
    tertiaryContainer = Pink80,
    onTertiaryContainer = Pink40,

    background = Color(0xFFFFFBFE),
    onBackground = Color(0xFF1C1B1F),

    surface = Color(0xFFFFFBFE),
    onSurface = Color(0xFF1C1B1F),

    error = Color(0xFFB3261E),
    onError = Color.White
)

// Paleta Dark
private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    onPrimary = Purple40,
    primaryContainer = Purple40,
    onPrimaryContainer = Purple80,

    secondary = PurpleGrey80,
    onSecondary = PurpleGrey40,
    secondaryContainer = PurpleGrey40,
    onSecondaryContainer = PurpleGrey80,

    tertiary = Pink80,
    onTertiary = Pink40,
    tertiaryContainer = Pink40,
    onTertiaryContainer = Pink80,

    background = Color(0xFF1C1B1F),
    onBackground = Color(0xFFE6E1E5),

    surface = Color(0xFF1C1B1F),
    onSurface = Color(0xFFE6E1E5),

    error = Color(0xFFF2B8B5),
    onError = Color(0xFF601410)
)
```

#### Crear Theme Composable

```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        // Dynamic color (Android 12+)
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        // Custom colors
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

#### Usar Colores del Tema

```kotlin
@Composable
fun ThemedComponentsExample() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Usar colores del tema
        Card(
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer,
                contentColor = MaterialTheme.colorScheme.onPrimaryContainer
            )
        ) {
            Text(
                text = "Primary Container",
                modifier = Modifier.padding(16.dp),
                style = MaterialTheme.typography.titleMedium
            )
        }

        Card(
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.secondaryContainer,
                contentColor = MaterialTheme.colorScheme.onSecondaryContainer
            )
        ) {
            Text(
                text = "Secondary Container",
                modifier = Modifier.padding(16.dp),
                style = MaterialTheme.typography.titleMedium
            )
        }

        Button(
            onClick = { },
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary
            )
        ) {
            Text("Primary Button")
        }

        Surface(
            color = MaterialTheme.colorScheme.surface,
            tonalElevation = 4.dp,
            shape = RoundedCornerShape(8.dp)
        ) {
            Text(
                text = "Surface con elevación",
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.onSurface
            )
        }
    }
}
```

---

### SwiftUI - Color Assets

#### Definir Colores en Asset Catalog

1. Abrir `Assets.xcassets`
2. Clic derecho → New Color Set
3. Nombrar color (ej: "PrimaryColor")
4. Configurar variantes Light/Dark

#### Definir Paleta en Código

```swift
import SwiftUI

extension Color {
    // Light mode colors
    static let primaryLight = Color(red: 0.4, green: 0.31, blue: 0.64)
    static let secondaryLight = Color(red: 0.38, green: 0.36, blue: 0.44)
    static let backgroundLight = Color(red: 1.0, green: 0.98, blue: 1.0)

    // Dark mode colors
    static let primaryDark = Color(red: 0.82, green: 0.74, blue: 1.0)
    static let secondaryDark = Color(red: 0.8, green: 0.76, blue: 0.86)
    static let backgroundDark = Color(red: 0.11, green: 0.11, blue: 0.12)

    // Adaptive colors
    static let primaryColor = Color("PrimaryColor") // Desde Assets
    static let secondaryColor = Color("SecondaryColor")
    static let customBackground = Color("BackgroundColor")
}
```

#### Usar Colores del Sistema

```swift
struct ThemedComponentsExample: View {
    @Environment(\.colorScheme) var colorScheme

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                // Colores del sistema (adaptativos)
                VStack(spacing: 8) {
                    ColorRow(color: .primary, name: "Primary")
                    ColorRow(color: .secondary, name: "Secondary")
                    ColorRow(color: .accentColor, name: "Accent")
                }

                // Colores de UI
                VStack(spacing: 8) {
                    ColorRow(color: Color(.systemBackground), name: "System Background")
                    ColorRow(color: Color(.secondarySystemBackground), name: "Secondary Background")
                    ColorRow(color: Color(.tertiarySystemBackground), name: "Tertiary Background")
                }

                // Colores de texto
                VStack(spacing: 8) {
                    ColorRow(color: Color(.label), name: "Label")
                    ColorRow(color: Color(.secondaryLabel), name: "Secondary Label")
                    ColorRow(color: Color(.tertiaryLabel), name: "Tertiary Label")
                }

                // Colores personalizados
                VStack(spacing: 8) {
                    ColorRow(color: .primaryColor, name: "Primary Color (Custom)")
                    ColorRow(color: .secondaryColor, name: "Secondary Color (Custom)")
                }

                Text("Modo actual: \(colorScheme == .dark ? "Oscuro" : "Claro")")
                    .font(.headline)
                    .padding()
            }
            .padding()
        }
    }
}

struct ColorRow: View {
    let color: Color
    let name: String

    var body: some View {
        HStack {
            RoundedRectangle(cornerRadius: 8)
                .fill(color)
                .frame(width: 50, height: 50)

            Text(name)
                .font(.body)

            Spacer()
        }
        .padding(.horizontal)
    }
}
```

---

## 🌙 Dark Mode

### Jetpack Compose - Detectar y Aplicar

#### Toggle Manual

```kotlin
@Composable
fun DarkModeToggleExample() {
    var isDarkMode by remember { mutableStateOf(false) }

    MyAppTheme(darkTheme = isDarkMode) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Dark Mode Demo") },
                    actions = {
                        IconButton(onClick = { isDarkMode = !isDarkMode }) {
                            Icon(
                                imageVector = if (isDarkMode) Icons.Default.LightMode
                                else Icons.Default.DarkMode,
                                contentDescription = "Toggle theme"
                            )
                        }
                    }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.primaryContainer
                    )
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            "Modo actual: ${if (isDarkMode) "Oscuro" else "Claro"}",
                            style = MaterialTheme.typography.titleLarge,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )

                        Spacer(modifier = Modifier.height(8.dp))

                        Text(
                            "Los colores se adaptan automáticamente al tema",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                }

                Button(
                    onClick = { },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Botón con colores temáticos")
                }

                OutlinedButton(
                    onClick = { },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Botón outlined")
                }

                Text(
                    "Texto con color primario",
                    color = MaterialTheme.colorScheme.primary,
                    style = MaterialTheme.typography.titleMedium
                )

                Text(
                    "Texto normal",
                    color = MaterialTheme.colorScheme.onBackground
                )
            }
        }
    }
}
```

#### Persistir Preferencia

```kotlin
// En ViewModel
class ThemeViewModel : ViewModel() {
    private val _isDarkMode = MutableStateFlow(false)
    val isDarkMode: StateFlow<Boolean> = _isDarkMode.asStateFlow()

    fun toggleTheme() {
        _isDarkMode.value = !_isDarkMode.value
        // Guardar en DataStore o SharedPreferences
    }

    fun loadThemePreference() {
        // Cargar desde DataStore o SharedPreferences
    }
}

// En MainActivity
@Composable
fun App(viewModel: ThemeViewModel = viewModel()) {
    val isDarkMode by viewModel.isDarkMode.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.loadThemePreference()
    }

    MyAppTheme(darkTheme = isDarkMode) {
        // App content
    }
}
```

---

### SwiftUI - Dark Mode

#### Toggle Manual

```swift
struct DarkModeToggleExample: View {
    @State private var isDarkMode = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 16) {
                    VStack(spacing: 8) {
                        Text("Modo actual: \(isDarkMode ? "Oscuro" : "Claro")")
                            .font(.title2)
                            .fontWeight(.bold)

                        Text("Los colores se adaptan automáticamente al tema")
                            .font(.body)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color(.secondarySystemBackground))
                    .cornerRadius(12)

                    Button("Botón con colores temáticos") {
                        // Action
                    }
                    .buttonStyle(.borderedProminent)
                    .frame(maxWidth: .infinity)

                    Button("Botón outlined") {
                        // Action
                    }
                    .buttonStyle(.bordered)
                    .frame(maxWidth: .infinity)

                    Text("Texto con color primario")
                        .foregroundColor(.accentColor)
                        .font(.headline)

                    Text("Texto normal")
                        .foregroundColor(.primary)
                }
                .padding()
            }
            .navigationTitle("Dark Mode Demo")
            .toolbar {
                Button(action: {
                    isDarkMode.toggle()
                }) {
                    Image(systemName: isDarkMode ? "sun.max" : "moon")
                }
            }
        }
        .preferredColorScheme(isDarkMode ? .dark : .light)
    }
}
```

#### Persistir Preferencia con AppStorage

```swift
struct App: View {
    @AppStorage("isDarkMode") private var isDarkMode = false

    var body: some View {
        ContentView()
            .preferredColorScheme(isDarkMode ? .dark : .light)
    }
}

struct SettingsView: View {
    @AppStorage("isDarkMode") private var isDarkMode = false

    var body: some View {
        Form {
            Section("Apariencia") {
                Toggle("Modo Oscuro", isOn: $isDarkMode)
            }
        }
        .navigationTitle("Ajustes")
    }
}
```

---

## ✍️ Tipografía

### Jetpack Compose - Typography

```kotlin
import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

// Definir familia de fuentes personalizada
val MyFontFamily = FontFamily(
    Font(R.font.my_font_regular, FontWeight.Normal),
    Font(R.font.my_font_bold, FontWeight.Bold),
    Font(R.font.my_font_medium, FontWeight.Medium)
)

// Definir tipografía personalizada
val Typography = Typography(
    displayLarge = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 57.sp,
        lineHeight = 64.sp
    ),
    displayMedium = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 45.sp,
        lineHeight = 52.sp
    ),
    headlineLarge = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 40.sp
    ),
    titleLarge = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 22.sp,
        lineHeight = 28.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp
    ),
    labelLarge = TextStyle(
        fontFamily = MyFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp
    )
)

@Composable
fun TypographyExample() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text("Display Large", style = MaterialTheme.typography.displayLarge)
        Text("Display Medium", style = MaterialTheme.typography.displayMedium)
        Text("Headline Large", style = MaterialTheme.typography.headlineLarge)
        Text("Title Large", style = MaterialTheme.typography.titleLarge)
        Text("Title Medium", style = MaterialTheme.typography.titleMedium)
        Text("Body Large", style = MaterialTheme.typography.bodyLarge)
        Text("Body Medium", style = MaterialTheme.typography.bodyMedium)
        Text("Label Large", style = MaterialTheme.typography.labelLarge)
    }
}
```

---

### SwiftUI - Custom Fonts

```swift
import SwiftUI

// Extensión para fuentes personalizadas
extension Font {
    static func customFont(size: CGFloat, weight: Font.Weight = .regular) -> Font {
        // Si tienes fuentes custom en Assets
        // return .custom("MyFontName", size: size)

        // Usando fuentes del sistema con peso
        return .system(size: size, weight: weight)
    }

    // Definir estilos personalizados
    static let displayLarge = customFont(size: 57, weight: .bold)
    static let displayMedium = customFont(size: 45, weight: .bold)
    static let headlineLarge = customFont(size: 32, weight: .bold)
    static let titleLarge = customFont(size: 22, weight: .bold)
    static let bodyLarge = customFont(size: 16, weight: .regular)
    static let bodyMedium = customFont(size: 14, weight: .regular)
    static let labelLarge = customFont(size: 14, weight: .medium)
}

struct TypographyExample: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
                Text("Display Large")
                    .font(.displayLarge)

                Text("Display Medium")
                    .font(.displayMedium)

                Text("Headline Large")
                    .font(.headlineLarge)

                Text("Title Large")
                    .font(.titleLarge)

                Text("Title Medium")
                    .font(.title2)

                Text("Body Large")
                    .font(.bodyLarge)

                Text("Body Medium")
                    .font(.bodyMedium)

                Text("Label Large")
                    .font(.labelLarge)

                Divider()

                Text("Fuentes del sistema:")
                    .font(.headline)

                Text("Large Title").font(.largeTitle)
                Text("Title").font(.title)
                Text("Title 2").font(.title2)
                Text("Title 3").font(.title3)
                Text("Headline").font(.headline)
                Text("Body").font(.body)
                Text("Callout").font(.callout)
                Text("Subheadline").font(.subheadline)
                Text("Footnote").font(.footnote)
                Text("Caption").font(.caption)
                Text("Caption 2").font(.caption2)
            }
            .padding()
        }
    }
}
```

---

## 🎨 Ejemplo Completo: Theme Switcher App

### Jetpack Compose

```kotlin
enum class AppTheme {
    LIGHT, DARK, SYSTEM
}

data class ThemeSettings(
    val theme: AppTheme = AppTheme.SYSTEM,
    val useDynamicColor: Boolean = true
)

class ThemeViewModel : ViewModel() {
    private val _settings = MutableStateFlow(ThemeSettings())
    val settings: StateFlow<ThemeSettings> = _settings.asStateFlow()

    fun setTheme(theme: AppTheme) {
        _settings.value = _settings.value.copy(theme = theme)
    }

    fun toggleDynamicColor() {
        _settings.value = _settings.value.copy(
            useDynamicColor = !_settings.value.useDynamicColor
        )
    }
}

@Composable
fun ThemeSwitcherApp(viewModel: ThemeViewModel = viewModel()) {
    val settings by viewModel.settings.collectAsState()

    val isDarkTheme = when (settings.theme) {
        AppTheme.LIGHT -> false
        AppTheme.DARK -> true
        AppTheme.SYSTEM -> isSystemInDarkTheme()
    }

    MyAppTheme(
        darkTheme = isDarkTheme,
        dynamicColor = settings.useDynamicColor
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Theme Switcher") }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp)
            ) {
                Text(
                    "Selecciona un tema",
                    style = MaterialTheme.typography.titleLarge,
                    modifier = Modifier.padding(bottom = 16.dp)
                )

                // Theme selector
                AppTheme.values().forEach { theme ->
                    ThemeOption(
                        theme = theme,
                        isSelected = settings.theme == theme,
                        onClick = { viewModel.setTheme(theme) }
                    )
                }

                Divider(modifier = Modifier.padding(vertical = 16.dp))

                // Dynamic color toggle (Android 12+)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                "Colores dinámicos",
                                style = MaterialTheme.typography.titleMedium
                            )
                            Text(
                                "Usar colores del wallpaper",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }

                        Switch(
                            checked = settings.useDynamicColor,
                            onCheckedChange = { viewModel.toggleDynamicColor() }
                        )
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))

                // Preview
                Text(
                    "Vista previa",
                    style = MaterialTheme.typography.titleLarge,
                    modifier = Modifier.padding(bottom = 16.dp)
                )

                ThemePreview()
            }
        }
    }
}

@Composable
fun ThemeOption(
    theme: AppTheme,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) {
                MaterialTheme.colorScheme.primaryContainer
            } else {
                MaterialTheme.colorScheme.surface
            }
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = when (theme) {
                        AppTheme.LIGHT -> Icons.Default.LightMode
                        AppTheme.DARK -> Icons.Default.DarkMode
                        AppTheme.SYSTEM -> Icons.Default.Brightness4
                    },
                    contentDescription = null
                )

                Spacer(modifier = Modifier.width(16.dp))

                Text(
                    text = when (theme) {
                        AppTheme.LIGHT -> "Claro"
                        AppTheme.DARK -> "Oscuro"
                        AppTheme.SYSTEM -> "Sistema"
                    }
                )
            }

            if (isSelected) {
                Icon(
                    imageVector = Icons.Default.Check,
                    contentDescription = "Selected",
                    tint = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@Composable
fun ThemePreview() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                "Título de ejemplo",
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.onSurface
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                "Este es un ejemplo de cómo se ven los textos con el tema seleccionado.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(16.dp))

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = { }) {
                    Text("Primary")
                }

                OutlinedButton(onClick = { }) {
                    Text("Outlined")
                }

                FilledTonalButton(onClick = { }) {
                    Text("Tonal")
                }
            }
        }
    }
}
```

---

### SwiftUI

```swift
enum AppTheme: String, CaseIterable {
    case light = "Claro"
    case dark = "Oscuro"
    case system = "Sistema"

    var colorScheme: ColorScheme? {
        switch self {
        case .light: return .light
        case .dark: return .dark
        case .system: return nil
        }
    }

    var icon: String {
        switch self {
        case .light: return "sun.max"
        case .dark: return "moon"
        case .system: return "circle.lefthalf.filled"
        }
    }
}

struct ThemeSwitcherApp: View {
    @AppStorage("selectedTheme") private var selectedTheme: String = AppTheme.system.rawValue

    var currentTheme: AppTheme {
        AppTheme(rawValue: selectedTheme) ?? .system
    }

    var body: some View {
        NavigationView {
            List {
                Section {
                    ForEach(AppTheme.allCases, id: \.self) { theme in
                        ThemeOption(
                            theme: theme,
                            isSelected: currentTheme == theme
                        ) {
                            selectedTheme = theme.rawValue
                        }
                    }
                } header: {
                    Text("Selecciona un tema")
                }

                Section {
                    ThemePreview()
                } header: {
                    Text("Vista previa")
                }
            }
            .navigationTitle("Theme Switcher")
        }
        .preferredColorScheme(currentTheme.colorScheme)
    }
}

struct ThemeOption: View {
    let theme: AppTheme
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                Image(systemName: theme.icon)
                    .foregroundColor(.accentColor)

                Text(theme.rawValue)
                    .foregroundColor(.primary)

                Spacer()

                if isSelected {
                    Image(systemName: "checkmark")
                        .foregroundColor(.accentColor)
                        .fontWeight(.bold)
                }
            }
            .padding(.vertical, 4)
        }
    }
}

struct ThemePreview: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Título de ejemplo")
                .font(.title2)
                .fontWeight(.bold)

            Text("Este es un ejemplo de cómo se ven los textos con el tema seleccionado.")
                .font(.body)
                .foregroundColor(.secondary)

            HStack(spacing: 8) {
                Button("Primary") { }
                    .buttonStyle(.borderedProminent)

                Button("Outlined") { }
                    .buttonStyle(.bordered)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear un sistema de temas completo con múltiples paletas de colores.

### Requisitos

- 3 temas: Predeterminado, Azul, Rosa
- Dark mode para cada tema
- Selector de tema con vista previa
- Persistir selección
- Animar cambio de tema

### Bonus

- Dynamic color (Android 12+)
- Accent color personalizado
- Diferentes tipografías por tema

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **Theming**: [developer.android.com/jetpack/compose/designsystems/material3](https://developer.android.com/jetpack/compose/designsystems/material3)
- **Dynamic Colors**: [m3.material.io/styles/color/dynamic-color](https://m3.material.io/styles/color/dynamic-color)

### SwiftUI
- **Color**: [developer.apple.com/documentation/swiftui/color](https://developer.apple.com/documentation/swiftui/color)
- **Dark Mode**: [developer.apple.com/design/human-interface-guidelines/dark-mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

---

**Anterior:** [09_ANIMACIONES.md](09_ANIMACIONES.md)
**¡Curso Completo!** 🎉

