# 📦 Componentes Básicos

> **Jetpack Compose (Android) & SwiftUI (iOS) - Elementos de UI Fundamentales**

---

## 🎯 Objetivo

Dominar los componentes básicos de UI que usarás en el 90% de tus aplicaciones: Text, Button, Image, Spacer, y Divider.

---

## 📝 Text - Mostrar Texto

El componente más fundamental en cualquier app.

### Jetpack Compose

#### Uso Básico

```kotlin
@Composable
fun TextExamples() {
    Column(modifier = Modifier.padding(16.dp)) {
        // Texto simple
        Text("Hola Mundo")

        // Texto con propiedades
        Text(
            text = "Texto personalizado",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Blue
        )

        // Texto multilinea
        Text(
            text = "Este es un texto muy largo que se va a dividir " +
                   "en múltiples líneas automáticamente",
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
    }
}
```

#### Propiedades Principales

```kotlin
Text(
    text = "Ejemplo completo",

    // Tamaño y peso
    fontSize = 20.sp,                    // Tamaño de fuente
    fontWeight = FontWeight.Bold,        // Normal, Medium, Bold, etc.
    fontStyle = FontStyle.Italic,        // Normal, Italic
    fontFamily = FontFamily.Monospace,   // Default, SansSerif, Serif, Monospace

    // Color
    color = Color.Red,

    // Alineación
    textAlign = TextAlign.Center,        // Start, End, Center, Justify

    // Líneas
    maxLines = 1,                        // Máximo de líneas
    overflow = TextOverflow.Ellipsis,    // Clip, Ellipsis, Visible

    // Decoración
    textDecoration = TextDecoration.Underline,  // None, Underline, LineThrough

    // Espaciado
    letterSpacing = 2.sp,                // Espacio entre letras
    lineHeight = 28.sp                   // Altura de línea
)
```

#### Estilos de Material Design 3

```kotlin
import androidx.compose.material3.MaterialTheme

@Composable
fun MaterialTextStyles() {
    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Display Large", style = MaterialTheme.typography.displayLarge)
        Text("Display Medium", style = MaterialTheme.typography.displayMedium)
        Text("Display Small", style = MaterialTheme.typography.displaySmall)

        Text("Headline Large", style = MaterialTheme.typography.headlineLarge)
        Text("Headline Medium", style = MaterialTheme.typography.headlineMedium)
        Text("Headline Small", style = MaterialTheme.typography.headlineSmall)

        Text("Title Large", style = MaterialTheme.typography.titleLarge)
        Text("Title Medium", style = MaterialTheme.typography.titleMedium)
        Text("Title Small", style = MaterialTheme.typography.titleSmall)

        Text("Body Large", style = MaterialTheme.typography.bodyLarge)
        Text("Body Medium", style = MaterialTheme.typography.bodyMedium)
        Text("Body Small", style = MaterialTheme.typography.bodySmall)

        Text("Label Large", style = MaterialTheme.typography.labelLarge)
        Text("Label Medium", style = MaterialTheme.typography.labelMedium)
        Text("Label Small", style = MaterialTheme.typography.labelSmall)
    }
}
```

---

### SwiftUI

#### Uso Básico

```swift
struct TextExamples: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Texto simple
            Text("Hola Mundo")

            // Texto con propiedades
            Text("Texto personalizado")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.blue)

            // Texto multilinea
            Text("Este es un texto muy largo que se va a dividir en múltiples líneas automáticamente")
                .lineLimit(2)
                .truncationMode(.tail)
        }
        .padding()
    }
}
```

#### Propiedades Principales

```swift
Text("Ejemplo completo")

    // Tamaño y peso
    .font(.system(size: 20))               // Tamaño custom
    .fontWeight(.bold)                     // .regular, .medium, .bold, etc.
    .italic()                              // Cursiva
    .fontDesign(.monospaced)               // .default, .serif, .rounded, .monospaced

    // Color
    .foregroundColor(.red)

    // Alineación
    .multilineTextAlignment(.center)       // .leading, .center, .trailing

    // Líneas
    .lineLimit(1)                          // Máximo de líneas
    .truncationMode(.tail)                 // .head, .middle, .tail

    // Decoración
    .underline()                           // Subrayado
    .strikethrough()                       // Tachado

    // Espaciado
    .tracking(2)                           // Espacio entre letras
    .lineSpacing(10)                       // Espacio entre líneas
```

#### Estilos de Sistema

```swift
struct SystemTextStyles: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Large Title").font(.largeTitle)
            Text("Title").font(.title)
            Text("Title 2").font(.title2)
            Text("Title 3").font(.title3)
            Text("Headline").font(.headline)
            Text("Subheadline").font(.subheadline)
            Text("Body").font(.body)
            Text("Callout").font(.callout)
            Text("Caption").font(.caption)
            Text("Caption 2").font(.caption2)
            Text("Footnote").font(.footnote)
        }
        .padding()
    }
}
```

---

### Comparación Text

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Texto simple | `Text("Hola")` | `Text("Hola")` |
| Tamaño de fuente | `fontSize = 20.sp` | `.font(.system(size: 20))` |
| Negrita | `fontWeight = FontWeight.Bold` | `.fontWeight(.bold)` |
| Color | `color = Color.Red` | `.foregroundColor(.red)` |
| Máx. líneas | `maxLines = 2` | `.lineLimit(2)` |
| Ellipsis | `overflow = TextOverflow.Ellipsis` | `.truncationMode(.tail)` |

---

## 🔘 Button - Botones Interactivos

### Jetpack Compose

#### Uso Básico

```kotlin
@Composable
fun ButtonExamples() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Botón simple
        Button(onClick = { /* Acción */ }) {
            Text("Click Me")
        }

        // Botón con ícono
        Button(onClick = { /* Acción */ }) {
            Icon(
                imageVector = Icons.Default.Favorite,
                contentDescription = "Like"
            )
            Spacer(modifier = Modifier.width(8.dp))
            Text("Like")
        }

        // Botón deshabilitado
        Button(
            onClick = { /* Acción */ },
            enabled = false
        ) {
            Text("Disabled")
        }

        // Botón con colores custom
        Button(
            onClick = { /* Acción */ },
            colors = ButtonDefaults.buttonColors(
                containerColor = Color.Green,
                contentColor = Color.White
            )
        ) {
            Text("Custom Colors")
        }
    }
}
```

#### Tipos de Botones Material 3

```kotlin
@Composable
fun MaterialButtons() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Filled Button (default)
        Button(onClick = { }) {
            Text("Filled Button")
        }

        // Filled Tonal Button
        FilledTonalButton(onClick = { }) {
            Text("Tonal Button")
        }

        // Outlined Button
        OutlinedButton(onClick = { }) {
            Text("Outlined Button")
        }

        // Text Button
        TextButton(onClick = { }) {
            Text("Text Button")
        }

        // Elevated Button
        ElevatedButton(onClick = { }) {
            Text("Elevated Button")
        }
    }
}
```

#### Botón con Estado

```kotlin
@Composable
fun ButtonWithState() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Clicked $count times")
    }
}
```

---

### SwiftUI

#### Uso Básico

```swift
struct ButtonExamples: View {
    var body: some View {
        VStack(spacing: 12) {
            // Botón simple
            Button("Click Me") {
                // Acción
            }

            // Botón con ícono
            Button(action: {
                // Acción
            }) {
                Label("Like", systemImage: "heart.fill")
            }

            // Botón deshabilitado
            Button("Disabled") {
                // Acción
            }
            .disabled(true)

            // Botón con colores custom
            Button("Custom Colors") {
                // Acción
            }
            .foregroundColor(.white)
            .padding()
            .background(Color.green)
            .cornerRadius(8)
        }
        .padding()
    }
}
```

#### Estilos de Botones

```swift
struct ButtonStyles: View {
    var body: some View {
        VStack(spacing: 12) {
            // Automatic (default)
            Button("Automatic") { }

            // Bordered
            Button("Bordered") { }
                .buttonStyle(.bordered)

            // Bordered Prominent
            Button("Bordered Prominent") { }
                .buttonStyle(.borderedProminent)

            // Borderless
            Button("Borderless") { }
                .buttonStyle(.borderless)

            // Plain
            Button("Plain") { }
                .buttonStyle(.plain)
        }
        .padding()
    }
}
```

#### Botón con Estado

```swift
struct ButtonWithState: View {
    @State private var count = 0

    var body: some View {
        Button("Clicked \(count) times") {
            count += 1
        }
    }
}
```

---

### Comparación Button

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Botón simple | `Button(onClick = {})` | `Button("Text") {}` |
| Con ícono | `Icon() + Text()` dentro | `Label("Text", systemImage: "name")` |
| Deshabilitar | `enabled = false` | `.disabled(true)` |
| Colores custom | `colors = ButtonDefaults.buttonColors(...)` | `.background() + .foregroundColor()` |
| Estilo outlined | `OutlinedButton` | `.buttonStyle(.bordered)` |

---

## 🖼️ Image - Imágenes

### Jetpack Compose

#### Uso Básico

```kotlin
@Composable
fun ImageExamples() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Imagen desde recursos
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Logo"
        )

        // Imagen desde vector asset (iconos Material)
        Image(
            imageVector = Icons.Default.Star,
            contentDescription = "Star icon"
        )

        // Imagen con tamaño fijo
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Logo",
            modifier = Modifier.size(100.dp)
        )

        // Imagen circular
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Profile",
            modifier = Modifier
                .size(80.dp)
                .clip(CircleShape)
        )

        // Imagen con escala
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Cover",
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        )
    }
}
```

#### Content Scale Options

```kotlin
// ContentScale opciones:
ContentScale.Crop       // Recorta para llenar
ContentScale.Fit        // Ajusta manteniendo aspecto
ContentScale.FillWidth  // Llena el ancho
ContentScale.FillHeight // Llena la altura
ContentScale.Inside     // Dentro del contenedor
ContentScale.None       // Tamaño original
```

#### Imagen desde URL (con Coil)

Primero añade la dependencia en `build.gradle.kts`:

```kotlin
dependencies {
    implementation("io.coil-kt:coil-compose:2.5.0")
}
```

Luego usa:

```kotlin
import coil.compose.AsyncImage

@Composable
fun NetworkImage() {
    AsyncImage(
        model = "https://example.com/image.jpg",
        contentDescription = "Remote image",
        modifier = Modifier.size(200.dp)
    )
}
```

---

### SwiftUI

#### Uso Básico

```swift
struct ImageExamples: View {
    var body: some View {
        VStack(spacing: 12) {
            // Imagen desde Assets
            Image("logo")
                .resizable()
                .scaledToFit()
                .frame(width: 100, height: 100)

            // Imagen de sistema (SF Symbols)
            Image(systemName: "star.fill")
                .font(.largeTitle)
                .foregroundColor(.yellow)

            // Imagen con tamaño fijo
            Image("logo")
                .resizable()
                .frame(width: 100, height: 100)

            // Imagen circular
            Image("profile")
                .resizable()
                .scaledToFill()
                .frame(width: 80, height: 80)
                .clipShape(Circle())

            // Imagen con escala
            Image("cover")
                .resizable()
                .scaledToFill()
                .frame(height: 200)
                .clipped()
        }
        .padding()
    }
}
```

#### Scale Options

```swift
// Opciones de escala:
.scaledToFit()    // Ajusta manteniendo aspecto
.scaledToFill()   // Llena recortando
.aspectRatio(contentMode: .fit)   // Equivalente a scaledToFit()
.aspectRatio(contentMode: .fill)  // Equivalente a scaledToFill()
```

#### Imagen desde URL

```swift
struct NetworkImage: View {
    var body: some View {
        AsyncImage(url: URL(string: "https://example.com/image.jpg")) { image in
            image
                .resizable()
                .scaledToFit()
        } placeholder: {
            ProgressView()
        }
        .frame(width: 200, height: 200)
    }
}
```

---

### Comparación Image

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Desde recursos | `painterResource(R.drawable.name)` | `Image("name")` |
| Ícono sistema | `Icons.Default.Star` | `Image(systemName: "star.fill")` |
| Tamaño fijo | `Modifier.size(100.dp)` | `.frame(width: 100, height: 100)` |
| Escala | `contentScale = ContentScale.Crop` | `.scaledToFill()` |
| Circular | `.clip(CircleShape)` | `.clipShape(Circle())` |
| Desde URL | Coil: `AsyncImage` | Nativo: `AsyncImage` |

---

## 📏 Spacer - Espacio Flexible

### Jetpack Compose

```kotlin
@Composable
fun SpacerExamples() {
    // Espacio vertical fijo
    Column {
        Text("Arriba")
        Spacer(modifier = Modifier.height(16.dp))
        Text("Abajo")
    }

    // Espacio horizontal fijo
    Row {
        Text("Izquierda")
        Spacer(modifier = Modifier.width(16.dp))
        Text("Derecha")
    }

    // Espacio flexible (toma todo el espacio disponible)
    Row(modifier = Modifier.fillMaxWidth()) {
        Text("Izquierda")
        Spacer(modifier = Modifier.weight(1f))  // ← Empuja a los extremos
        Text("Derecha")
    }

    // Centrar con spacers
    Column(modifier = Modifier.fillMaxHeight()) {
        Spacer(modifier = Modifier.weight(1f))
        Text("Centrado verticalmente")
        Spacer(modifier = Modifier.weight(1f))
    }
}
```

---

### SwiftUI

```swift
struct SpacerExamples: View {
    var body: some View {
        VStack {
            // Espacio vertical fijo
            VStack(spacing: 0) {
                Text("Arriba")
                Spacer()
                    .frame(height: 16)
                Text("Abajo")
            }

            // Espacio horizontal fijo
            HStack(spacing: 0) {
                Text("Izquierda")
                Spacer()
                    .frame(width: 16)
                Text("Derecha")
            }

            // Espacio flexible (toma todo el espacio disponible)
            HStack {
                Text("Izquierda")
                Spacer()  // ← Empuja a los extremos
                Text("Derecha")
            }

            // Centrar con spacers
            VStack {
                Spacer()
                Text("Centrado verticalmente")
                Spacer()
            }
        }
    }
}
```

---

### Comparación Spacer

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Espacio vertical | `Spacer(Modifier.height(16.dp))` | `Spacer().frame(height: 16)` |
| Espacio horizontal | `Spacer(Modifier.width(16.dp))` | `Spacer().frame(width: 16)` |
| Espacio flexible | `Spacer(Modifier.weight(1f))` | `Spacer()` (sin frame) |

---

## ➖ Divider - Separadores

### Jetpack Compose

```kotlin
@Composable
fun DividerExamples() {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Sección 1")

        // Divider horizontal (default)
        Divider()

        Text("Sección 2")

        // Divider con color y grosor custom
        Divider(
            color = Color.Red,
            thickness = 2.dp
        )

        Text("Sección 3")

        // Divider con margen
        Divider(
            modifier = Modifier.padding(vertical = 8.dp),
            color = Color.Gray.copy(alpha = 0.5f)
        )

        Text("Sección 4")
    }
}

// Divider vertical (en Row)
@Composable
fun VerticalDividerExample() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(100.dp)
            .padding(16.dp)
    ) {
        Text("Izquierda")

        Divider(
            modifier = Modifier
                .fillMaxHeight()
                .width(1.dp)
                .padding(horizontal = 8.dp)
        )

        Text("Derecha")
    }
}
```

---

### SwiftUI

```swift
struct DividerExamples: View {
    var body: some View {
        VStack(spacing: 0) {
            Text("Sección 1")
                .padding()

            // Divider horizontal (default)
            Divider()

            Text("Sección 2")
                .padding()

            // Divider con color (requiere overlay)
            Divider()
                .background(Color.red)
                .frame(height: 2)

            Text("Sección 3")
                .padding()

            // Divider con margen
            Divider()
                .padding(.vertical, 8)

            Text("Sección 4")
                .padding()
        }
    }
}

// Divider vertical (en HStack)
struct VerticalDividerExample: View {
    var body: some View {
        HStack {
            Text("Izquierda")

            Divider()
                .frame(height: 100)
                .padding(.horizontal, 8)

            Text("Derecha")
        }
        .padding()
    }
}
```

---

### Comparación Divider

| Feature | Compose | SwiftUI |
|---------|---------|---------|
| Horizontal | `Divider()` | `Divider()` |
| Vertical | En `Row` con `.fillMaxHeight().width(1.dp)` | En `HStack` con `.frame(height: ...)` |
| Color | `color = Color.Red` | `.background(Color.red)` |
| Grosor | `thickness = 2.dp` | `.frame(height: 2)` |

---

## 🎨 Ejemplo Completo: Card de Usuario

Combinemos todos los componentes en un ejemplo real.

### Jetpack Compose

```kotlin
@Composable
fun UserCard() {
    var isFollowing by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Header con avatar y nombre
            Row(verticalAlignment = Alignment.CenterVertically) {
                // Avatar
                Image(
                    painter = painterResource(id = R.drawable.ic_launcher_foreground),
                    contentDescription = "Avatar",
                    modifier = Modifier
                        .size(60.dp)
                        .clip(CircleShape)
                        .background(Color.LightGray)
                )

                Spacer(modifier = Modifier.width(16.dp))

                // Nombre y username
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Juan Pérez",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "@juanperez",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.Gray
                    )
                }

                // Botón seguir
                Button(
                    onClick = { isFollowing = !isFollowing },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isFollowing) Color.Gray else Color.Blue
                    )
                ) {
                    Text(if (isFollowing) "Siguiendo" else "Seguir")
                }
            }

            Spacer(modifier = Modifier.height(12.dp))
            Divider()
            Spacer(modifier = Modifier.height(12.dp))

            // Bio
            Text(
                text = "Desarrollador móvil apasionado por crear experiencias increíbles. " +
                       "Jetpack Compose & SwiftUI enthusiast 📱",
                style = MaterialTheme.typography.bodyMedium
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Estadísticas
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem("1.2K", "Seguidores")
                StatItem("342", "Siguiendo")
                StatItem("89", "Posts")
            }
        }
    }
}

@Composable
fun StatItem(value: String, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = Color.Gray
        )
    }
}

@Preview(showBackground = true)
@Composable
fun UserCardPreview() {
    UserCard()
}
```

---

### SwiftUI

```swift
struct UserCard: View {
    @State private var isFollowing = false

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Header con avatar y nombre
            HStack(alignment: .center) {
                // Avatar
                Circle()
                    .fill(Color.gray.opacity(0.3))
                    .frame(width: 60, height: 60)
                    .overlay(
                        Image(systemName: "person.fill")
                            .foregroundColor(.gray)
                    )

                // Nombre y username
                VStack(alignment: .leading, spacing: 4) {
                    Text("Juan Pérez")
                        .font(.headline)
                        .fontWeight(.bold)
                    Text("@juanperez")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }

                Spacer()

                // Botón seguir
                Button(action: {
                    isFollowing.toggle()
                }) {
                    Text(isFollowing ? "Siguiendo" : "Seguir")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 20)
                        .padding(.vertical, 8)
                        .background(isFollowing ? Color.gray : Color.blue)
                        .cornerRadius(20)
                }
            }

            Divider()

            // Bio
            Text("Desarrollador móvil apasionado por crear experiencias increíbles. Jetpack Compose & SwiftUI enthusiast 📱")
                .font(.body)
                .fixedSize(horizontal: false, vertical: true)

            // Estadísticas
            HStack {
                Spacer()
                StatItem(value: "1.2K", label: "Seguidores")
                Spacer()
                StatItem(value: "342", label: "Siguiendo")
                Spacer()
                StatItem(value: "89", label: "Posts")
                Spacer()
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(radius: 4)
        .padding()
    }
}

struct StatItem: View {
    let value: String
    let label: String

    var body: some View {
        VStack(spacing: 4) {
            Text(value)
                .font(.headline)
                .fontWeight(.bold)
            Text(label)
                .font(.caption)
                .foregroundColor(.gray)
        }
    }
}

#Preview {
    UserCard()
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear una tarjeta de producto usando todos los componentes aprendidos.

### Requisitos

La tarjeta debe tener:
- ✅ Imagen del producto (usa un placeholder)
- ✅ Nombre del producto (Text, bold)
- ✅ Descripción breve (Text, gris)
- ✅ Precio (Text, grande, color primario)
- ✅ Divider
- ✅ Botón "Agregar al carrito"
- ✅ Botón de favorito (ícono de corazón)

### Bonus

- Implementa estado para el botón de favorito (relleno/vacío)
- Añade contador de cantidad con botones +/-
- Aplica shadow/elevation a la card

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **Text**: [developer.android.com/jetpack/compose/text](https://developer.android.com/jetpack/compose/text)
- **Button**: [developer.android.com/jetpack/compose/components/button](https://developer.android.com/jetpack/compose/components/button)
- **Image**: [developer.android.com/jetpack/compose/graphics/images](https://developer.android.com/jetpack/compose/graphics/images)
- **Material Icons**: [fonts.google.com/icons](https://fonts.google.com/icons)

### SwiftUI
- **Text**: [developer.apple.com/documentation/swiftui/text](https://developer.apple.com/documentation/swiftui/text)
- **Button**: [developer.apple.com/documentation/swiftui/button](https://developer.apple.com/documentation/swiftui/button)
- **Image**: [developer.apple.com/documentation/swiftui/image](https://developer.apple.com/documentation/swiftui/image)
- **SF Symbols**: [developer.apple.com/sf-symbols/](https://developer.apple.com/sf-symbols/)

---

**Anterior:** [02_SETUP_AMBIENTE.md](02_SETUP_AMBIENTE.md)
**Siguiente:** [04_LAYOUTS_BASICOS.md](04_LAYOUTS_BASICOS.md) - Layouts y contenedores

