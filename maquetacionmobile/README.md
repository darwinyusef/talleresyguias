# 📱 Guía Completa de Maquetación Mobile

> **Jetpack Compose (Android) & SwiftUI (iOS) - Side by Side**

---

## 🎯 Objetivo

Aprender a maquetar aplicaciones móviles modernas usando las últimas tecnologías declarativas:
- **Jetpack Compose** para Android (Kotlin)
- **SwiftUI** para iOS (Swift)

**¡En paralelo!** Cada concepto se enseña en ambas plataformas simultáneamente.

---

## 📚 Estructura del Curso

### 📗 Parte 1: Fundamentos
- **Introducción** - UI Declarativa vs Imperativa
- **Setup** - Android Studio + Xcode
- **Componentes Básicos** - Text, Button, Image
- **Layouts** - Column/Row, VStack/HStack
- **Modificadores** - Styling y personalización

### 📘 Parte 2: Layouts Avanzados
- **Lists** - LazyColumn vs List
- **Grids** - LazyVerticalGrid vs LazyVGrid
- **Navigation** - NavController vs NavigationStack
- **Tabs** - BottomNavigation vs TabView
- **Drawer** - Navigation Drawer vs Sidebar

### 📙 Parte 3: Estado y Datos
- **State Management** - remember vs @State
- **ViewModel** - MVVM en ambas plataformas
- **Data Flow** - MutableState vs Binding
- **Listas dinámicas** - RecyclerView vs List
- **Forms** - TextField validation

### 📕 Parte 4: Animaciones y Gestos
- **Animaciones básicas** - animate* vs withAnimation
- **Transiciones** - AnimatedVisibility vs transition
- **Gestos** - Modifier.clickable vs onTapGesture
- **Drag & Drop** - detectDragGestures vs DragGesture

### 📔 Parte 5: Temas y Estilos
- **Material Design 3** - Compose
- **Apple HIG** - SwiftUI
- **Dark Mode** - isSystemInDarkTheme vs colorScheme
- **Custom Themes** - MaterialTheme vs custom styles
- **Typography** - Font families

### 📓 Parte 6: Componentes Avanzados
- **Bottom Sheets** - ModalBottomSheet vs sheet
- **Dialogs** - AlertDialog vs Alert
- **Snackbars** - ScaffoldState vs Alert
- **Pull to Refresh** - SwipeRefresh vs refreshable
- **Paging** - Paging 3 vs LazyVStack

### 📒 Parte 7: Integración con APIs
- **Networking** - Retrofit vs URLSession
- **JSON Parsing** - Gson/Moshi vs Codable
- **Image Loading** - Coil vs AsyncImage
- **WebView** - AndroidView vs WKWebView
- **Camera** - CameraX vs PhotosPicker

### 📙 Parte 8: Proyectos Reales
- **App de Noticias** - Feed con imágenes
- **App de E-commerce** - Catálogo de productos
- **App Social** - Posts, likes, comments
- **App de Mapas** - Google Maps vs MapKit
- **App Full-Stack** - Frontend + Backend

---

## 🗺️ Roadmap de Aprendizaje

```
┌─────────────────────────────────────────┐
│    INICIO: Conceptos Fundamentales      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SEMANA 1: Componentes Básicos          │
│  • Text, Button, Image                  │
│  • Column/Row, VStack/HStack            │
│  • Modificadores                         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SEMANA 2: Layouts y Navegación         │
│  • Lists y Grids                        │
│  • Navigation                           │
│  • Tabs y Drawer                        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SEMANA 3: Estado y Datos               │
│  • State Management                     │
│  • ViewModel (MVVM)                     │
│  • Forms y Validación                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SEMANA 4: Proyecto Final               │
│  • App completa con API                 │
│  • Animaciones                          │
│  • Publicación                          │
└─────────────────────────────────────────┘
```

---

## 📖 Guías Disponibles

### 🟢 Nivel Principiante

1. **[01_INTRODUCCION_UI_DECLARATIVA.md](01_INTRODUCCION_UI_DECLARATIVA.md)**
   - ¿Qué es UI declarativa?
   - Comparación con UI imperativa
   - Ventajas y desventajas

2. **[02_SETUP_AMBIENTE.md](02_SETUP_AMBIENTE.md)**
   - Instalar Android Studio
   - Instalar Xcode
   - Primer proyecto

3. **[03_COMPONENTES_BASICOS.md](03_COMPONENTES_BASICOS.md)**
   - Text (Compose) vs Text (SwiftUI)
   - Button y eventos
   - Image y recursos
   - Spacer y Divider

4. **[04_LAYOUTS_BASICOS.md](04_LAYOUTS_BASICOS.md)**
   - Column vs VStack
   - Row vs HStack
   - Box vs ZStack
   - Arrangement y Alignment

### 🟡 Nivel Intermedio

5. **[05_LISTAS_Y_GRIDS.md](05_LISTAS_Y_GRIDS.md)**
   - LazyColumn vs List
   - LazyRow vs ScrollView
   - LazyVerticalGrid vs LazyVGrid
   - Items dinámicos

6. **[06_NAVEGACION.md](06_NAVEGACION.md)**
   - NavController vs NavigationStack
   - Pasar datos entre pantallas
   - Deep linking
   - Bottom Navigation vs TabView

7. **[07_STATE_MANAGEMENT.md](07_STATE_MANAGEMENT.md)**
   - remember vs @State
   - mutableStateOf vs @Binding
   - ViewModel pattern
   - StateFlow vs @Published

8. **[08_FORMULARIOS.md](08_FORMULARIOS.md)**
   - TextField vs TextField
   - Validación
   - Keyboard types
   - Focus management

### 🔴 Nivel Avanzado

9. **[09_ANIMACIONES.md](09_ANIMACIONES.md)**
   - Animaciones básicas
   - Transiciones
   - Animaciones complejas
   - Spring animations

10. **[10_TEMAS_Y_ESTILOS.md](10_TEMAS_Y_ESTILOS.md)**
    - Material Design 3
    - Apple HIG
    - Dark mode
    - Custom themes

11. **[11_COMPONENTES_AVANZADOS.md](11_COMPONENTES_AVANZADOS.md)**
    - Bottom Sheets
    - Dialogs y Alerts
    - Pull to Refresh
    - Custom Components

12. **[12_INTEGRACION_APIS.md](12_INTEGRACION_APIS.md)**
    - Retrofit vs URLSession
    - JSON parsing
    - Image loading
    - Error handling

### 🚀 Proyectos

13. **[PROYECTO_01_APP_NOTICIAS.md](PROYECTO_01_APP_NOTICIAS.md)**
    - Feed de noticias
    - Categorías
    - Detalle de noticia
    - Favoritos

14. **[PROYECTO_02_APP_ECOMMERCE.md](PROYECTO_02_APP_ECOMMERCE.md)**
    - Catálogo de productos
    - Carrito de compras
    - Checkout
    - Historial de pedidos

15. **[PROYECTO_03_APP_SOCIAL.md](PROYECTO_03_APP_SOCIAL.md)**
    - Feed de posts
    - Likes y comentarios
    - Perfil de usuario
    - Mensajería

---

## 🎨 Formato de las Guías

Cada guía sigue esta estructura:

```markdown
# Tema

## Jetpack Compose (Android)
### Código
### Explicación
### Resultado

## SwiftUI (iOS)
### Código
### Explicación
### Resultado

## Comparación
### Similitudes
### Diferencias
### ¿Cuándo usar qué?

## Ejercicio Práctico
```

---

## 💻 Requisitos

### Para Android (Jetpack Compose)
- **Android Studio**: Giraffe o superior
- **JDK**: 17+
- **Kotlin**: 1.9+
- **Compose**: 1.5+
- **OS**: Windows, macOS o Linux

### Para iOS (SwiftUI)
- **Xcode**: 15+
- **Swift**: 5.9+
- **macOS**: Ventura (13) o superior
- **iOS Target**: 16+

### Conocimientos Previos
- ✅ Programación básica
- ✅ Kotlin básico (para Compose)
- ✅ Swift básico (para SwiftUI)
- ⚠️ No es necesario saber Android/iOS tradicional

---

## 🎯 Tabla Comparativa Rápida

| Concepto | Jetpack Compose | SwiftUI |
|----------|----------------|---------|
| **Lenguaje** | Kotlin | Swift |
| **Paradigma** | Declarativo | Declarativo |
| **Vertical Stack** | `Column` | `VStack` |
| **Horizontal Stack** | `Row` | `HStack` |
| **Overlay Stack** | `Box` | `ZStack` |
| **Lista** | `LazyColumn` | `List` |
| **Grid** | `LazyVerticalGrid` | `LazyVGrid` |
| **Navegación** | `NavController` | `NavigationStack` |
| **Estado** | `remember`, `mutableStateOf` | `@State` |
| **Binding** | `MutableState` | `@Binding` |
| **Observable** | `StateFlow` | `@Published` |
| **ViewModel** | `ViewModel` | `ObservableObject` |
| **Botón** | `Button` | `Button` |
| **Texto** | `Text` | `Text` |
| **Imagen** | `Image` | `Image` |
| **Input** | `TextField` | `TextField` |
| **Modificadores** | `.modifier()` | `.modifier()` |
| **Padding** | `.padding()` | `.padding()` |
| **Background** | `.background()` | `.background()` |
| **Animación** | `animateAsState` | `withAnimation` |
| **Tema** | `MaterialTheme` | `@Environment` |
| **Preview** | `@Preview` | `#Preview` |

---

## 🚀 Quick Start

### Android (Jetpack Compose)

```kotlin
// MainActivity.kt
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApp()
        }
    }
}

@Composable
fun MyApp() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("¡Hola Jetpack Compose!")
        Button(onClick = { /* Acción */ }) {
            Text("Click Me")
        }
    }
}
```

### iOS (SwiftUI)

```swift
// ContentView.swift
struct ContentView: View {
    var body: some View {
        VStack {
            Text("¡Hola SwiftUI!")
            Button("Click Me") {
                // Acción
            }
        }
    }
}
```

---

## 📊 Progreso Recomendado

### Semana 1: Fundamentos
- [ ] Introducción a UI declarativa
- [ ] Setup del ambiente
- [ ] Componentes básicos
- [ ] Layouts básicos

### Semana 2: Navegación y Listas
- [ ] Listas y Grids
- [ ] Navegación entre pantallas
- [ ] Tabs y Drawer

### Semana 3: Estado y Datos
- [ ] State Management
- [ ] ViewModel (MVVM)
- [ ] Formularios
- [ ] Integración con APIs

### Semana 4: Proyecto Final
- [ ] Elegir proyecto
- [ ] Implementar
- [ ] Publicar

---

## 🎓 Certificación

Al completar:
- ✅ Todas las guías (1-12)
- ✅ Ejercicios prácticos
- ✅ 2 de 3 proyectos

Estarás listo para:
- 🎯 Desarrollar apps Android con Jetpack Compose
- 🎯 Desarrollar apps iOS con SwiftUI
- 🎯 Posición: Junior Mobile Developer
- 🎯 Freelancing en desarrollo móvil

---

## 📚 Recursos Adicionales

### Documentación Oficial
- **Jetpack Compose**: https://developer.android.com/jetpack/compose
- **SwiftUI**: https://developer.apple.com/xcode/swiftui/

### Comunidades
- **Reddit**: r/androiddev, r/iOSProgramming
- **Discord**: Android Dev, iOS Dev
- **Stack Overflow**: Tags [jetpack-compose], [swiftui]

### Cursos Complementarios
- Google Codelabs (Jetpack Compose)
- Apple Tutorials (SwiftUI)
- Udemy, Coursera

---

## 🤝 Contribuir

¿Encontraste un error? ¿Quieres añadir un ejemplo?

1. Fork el repositorio
2. Crea tu branch
3. Envía Pull Request

---

## 📞 Soporte

- 📧 Email: support@example.com
- 💬 Discord: [Link]
- 🐦 Twitter: @mobiledevelopers

---

**¡Comienza tu viaje en desarrollo móvil! 📱✨**

Siguiente: [01_INTRODUCCION_UI_DECLARATIVA.md](01_INTRODUCCION_UI_DECLARATIVA.md)
