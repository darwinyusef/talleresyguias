# 📐 Layouts Básicos

> **Jetpack Compose (Android) & SwiftUI (iOS) - Contenedores y Organización**

---

## 🎯 Objetivo

Dominar los contenedores fundamentales para organizar elementos en la pantalla: layouts verticales, horizontales y en capas (overlay).

---

## 📊 Conceptos Fundamentales

### ¿Qué es un Layout?

Un **layout** es un contenedor que organiza múltiples elementos hijos según reglas específicas.

### Los 3 Layouts Esenciales

| Propósito | Compose | SwiftUI |
|-----------|---------|---------|
| **Apilar verticalmente** | `Column` | `VStack` |
| **Apilar horizontalmente** | `Row` | `HStack` |
| **Superponer (overlay)** | `Box` | `ZStack` |

---

## 📦 Column / VStack - Layout Vertical

Organiza elementos de arriba hacia abajo.

### Jetpack Compose - Column

#### Uso Básico

```kotlin
@Composable
fun ColumnExample() {
    Column {
        Text("Primero")
        Text("Segundo")
        Text("Tercero")
    }
}
```

#### Con Modificadores

```kotlin
@Composable
fun ColumnWithModifiers() {
    Column(
        // Tamaño
        modifier = Modifier
            .fillMaxSize()           // Llenar toda la pantalla
            .padding(16.dp)          // Margen interno
            .background(Color.LightGray),

        // Alineación horizontal de los hijos
        horizontalAlignment = Alignment.CenterHorizontally,  // Start, CenterHorizontally, End

        // Distribución vertical
        verticalArrangement = Arrangement.Center  // Top, Center, Bottom, SpaceBetween, etc.
    ) {
        Text("Texto 1")
        Text("Texto 2")
        Text("Texto 3")
    }
}
```

#### Opciones de Alineación Horizontal

```kotlin
@Composable
fun ColumnAlignments() {
    Column(modifier = Modifier.fillMaxWidth()) {
        // Alineación a la izquierda (default)
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.Start
        ) {
            Text("Alineado a la izquierda")
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Alineación al centro
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Centrado")
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Alineación a la derecha
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.End
        ) {
            Text("Alineado a la derecha")
        }
    }
}
```

#### Opciones de Arrangement Vertical

```kotlin
@Composable
fun ColumnArrangements() {
    // Top (default) - Elementos arriba
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Top
    ) {
        Text("A"); Text("B"); Text("C")
    }

    // Center - Elementos en el centro
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center
    ) {
        Text("A"); Text("B"); Text("C")
    }

    // Bottom - Elementos abajo
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Bottom
    ) {
        Text("A"); Text("B"); Text("C")
    }

    // SpaceBetween - Espacio entre elementos
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Text("A"); Text("B"); Text("C")
    }

    // SpaceAround - Espacio alrededor de elementos
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.SpaceAround
    ) {
        Text("A"); Text("B"); Text("C")
    }

    // SpaceEvenly - Espacio igual entre todos
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.SpaceEvenly
    ) {
        Text("A"); Text("B"); Text("C")
    }

    // spacedBy - Espacio fijo entre elementos
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("A"); Text("B"); Text("C")
    }
}
```

---

### SwiftUI - VStack

#### Uso Básico

```swift
struct VStackExample: View {
    var body: some View {
        VStack {
            Text("Primero")
            Text("Segundo")
            Text("Tercero")
        }
    }
}
```

#### Con Modificadores

```swift
struct VStackWithModifiers: View {
    var body: some View {
        VStack(
            alignment: .center,      // .leading, .center, .trailing
            spacing: 16              // Espacio entre elementos
        ) {
            Text("Texto 1")
            Text("Texto 2")
            Text("Texto 3")
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)  // Llenar pantalla
        .padding()                   // Margen interno
        .background(Color.gray.opacity(0.2))
    }
}
```

#### Opciones de Alineación

```swift
struct VStackAlignments: View {
    var body: some View {
        VStack(spacing: 20) {
            // Alineación a la izquierda
            VStack(alignment: .leading) {
                Text("Alineado a la izquierda")
            }
            .frame(maxWidth: .infinity)
            .background(Color.blue.opacity(0.1))

            // Alineación al centro (default)
            VStack(alignment: .center) {
                Text("Centrado")
            }
            .frame(maxWidth: .infinity)
            .background(Color.green.opacity(0.1))

            // Alineación a la derecha
            VStack(alignment: .trailing) {
                Text("Alineado a la derecha")
            }
            .frame(maxWidth: .infinity)
            .background(Color.red.opacity(0.1))
        }
    }
}
```

#### Distribución Vertical con Spacers

```swift
struct VStackDistribution: View {
    var body: some View {
        VStack {
            // Top (default)
            Text("A"); Text("B"); Text("C")

            // Center con Spacers
            Spacer()
            Text("A"); Text("B"); Text("C")
            Spacer()

            // Bottom con Spacer
            Spacer()
            Text("A"); Text("B"); Text("C")

            // SpaceBetween con múltiples Spacers
            Text("A")
            Spacer()
            Text("B")
            Spacer()
            Text("C")

            // Espaciado fijo
            VStack(spacing: 16) {
                Text("A"); Text("B"); Text("C")
            }
        }
        .frame(maxHeight: .infinity)
    }
}
```

---

### Comparación Column / VStack

| Feature | Compose (Column) | SwiftUI (VStack) |
|---------|------------------|------------------|
| Uso básico | `Column { }` | `VStack { }` |
| Alineación horizontal | `horizontalAlignment = Alignment.CenterHorizontally` | `alignment: .center` |
| Espacio entre items | `verticalArrangement = Arrangement.spacedBy(16.dp)` | `spacing: 16` |
| Llenar pantalla | `Modifier.fillMaxSize()` | `.frame(maxHeight: .infinity)` |
| Centro vertical | `verticalArrangement = Arrangement.Center` | Usar `Spacer()` arriba y abajo |

---

## ➡️ Row / HStack - Layout Horizontal

Organiza elementos de izquierda a derecha.

### Jetpack Compose - Row

#### Uso Básico

```kotlin
@Composable
fun RowExample() {
    Row {
        Text("A")
        Text("B")
        Text("C")
    }
}
```

#### Con Modificadores

```kotlin
@Composable
fun RowWithModifiers() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .background(Color.LightGray),

        // Alineación vertical de los hijos
        verticalAlignment = Alignment.CenterVertically,  // Top, CenterVertically, Bottom

        // Distribución horizontal
        horizontalArrangement = Arrangement.Center  // Start, Center, End, SpaceBetween, etc.
    ) {
        Text("Texto 1")
        Text("Texto 2")
        Text("Texto 3")
    }
}
```

#### Opciones de Alineación Vertical

```kotlin
@Composable
fun RowAlignments() {
    Column {
        // Alineación arriba
        Row(
            modifier = Modifier.fillMaxWidth().height(100.dp).background(Color.LightGray),
            verticalAlignment = Alignment.Top
        ) {
            Text("Top")
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Alineación centro (default)
        Row(
            modifier = Modifier.fillMaxWidth().height(100.dp).background(Color.LightGray),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Center")
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Alineación abajo
        Row(
            modifier = Modifier.fillMaxWidth().height(100.dp).background(Color.LightGray),
            verticalAlignment = Alignment.Bottom
        ) {
            Text("Bottom")
        }
    }
}
```

#### Opciones de Arrangement Horizontal

```kotlin
@Composable
fun RowArrangements() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Start (default)
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.Start
        ) {
            Text("A"); Text("B"); Text("C")
        }

        // Center
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.Center
        ) {
            Text("A"); Text("B"); Text("C")
        }

        // End
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.End
        ) {
            Text("A"); Text("B"); Text("C")
        }

        // SpaceBetween
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("A"); Text("B"); Text("C")
        }

        // SpaceAround
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.SpaceAround
        ) {
            Text("A"); Text("B"); Text("C")
        }

        // SpaceEvenly
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Text("A"); Text("B"); Text("C")
        }

        // spacedBy (espacio fijo)
        Row(
            modifier = Modifier.fillMaxWidth().background(Color.LightGray),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text("A"); Text("B"); Text("C")
        }
    }
}
```

#### Weight - Distribución Proporcional

```kotlin
@Composable
fun RowWithWeights() {
    Row(modifier = Modifier.fillMaxWidth()) {
        // Primer elemento toma 1/4 del espacio
        Text(
            "25%",
            modifier = Modifier
                .weight(1f)
                .background(Color.Red)
        )

        // Segundo elemento toma 3/4 del espacio
        Text(
            "75%",
            modifier = Modifier
                .weight(3f)
                .background(Color.Blue)
        )
    }

    // Weights iguales (distribución equitativa)
    Row(modifier = Modifier.fillMaxWidth()) {
        Text("33%", modifier = Modifier.weight(1f).background(Color.Red))
        Text("33%", modifier = Modifier.weight(1f).background(Color.Green))
        Text("33%", modifier = Modifier.weight(1f).background(Color.Blue))
    }
}
```

---

### SwiftUI - HStack

#### Uso Básico

```swift
struct HStackExample: View {
    var body: some View {
        HStack {
            Text("A")
            Text("B")
            Text("C")
        }
    }
}
```

#### Con Modificadores

```swift
struct HStackWithModifiers: View {
    var body: some View {
        HStack(
            alignment: .center,      // .top, .center, .bottom
            spacing: 16              // Espacio entre elementos
        ) {
            Text("Texto 1")
            Text("Texto 2")
            Text("Texto 3")
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.gray.opacity(0.2))
    }
}
```

#### Opciones de Alineación Vertical

```swift
struct HStackAlignments: View {
    var body: some View {
        VStack(spacing: 8) {
            // Alineación arriba
            HStack(alignment: .top) {
                Text("Top")
                Text("Alignment")
            }
            .frame(maxWidth: .infinity, minHeight: 60)
            .background(Color.gray.opacity(0.2))

            // Alineación centro (default)
            HStack(alignment: .center) {
                Text("Center")
                Text("Alignment")
            }
            .frame(maxWidth: .infinity, minHeight: 60)
            .background(Color.gray.opacity(0.2))

            // Alineación abajo
            HStack(alignment: .bottom) {
                Text("Bottom")
                Text("Alignment")
            }
            .frame(maxWidth: .infinity, minHeight: 60)
            .background(Color.gray.opacity(0.2))
        }
    }
}
```

#### Distribución Horizontal con Spacers

```swift
struct HStackDistribution: View {
    var body: some View {
        VStack(spacing: 8) {
            // Leading (default)
            HStack {
                Text("A"); Text("B"); Text("C")
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color.gray.opacity(0.2))

            // Center
            HStack {
                Text("A"); Text("B"); Text("C")
            }
            .frame(maxWidth: .infinity, alignment: .center)
            .background(Color.gray.opacity(0.2))

            // Trailing
            HStack {
                Text("A"); Text("B"); Text("C")
            }
            .frame(maxWidth: .infinity, alignment: .trailing)
            .background(Color.gray.opacity(0.2))

            // SpaceBetween con Spacers
            HStack {
                Text("A")
                Spacer()
                Text("B")
                Spacer()
                Text("C")
            }
            .frame(maxWidth: .infinity)
            .background(Color.gray.opacity(0.2))

            // Espaciado fijo
            HStack(spacing: 16) {
                Text("A"); Text("B"); Text("C")
            }
            .frame(maxWidth: .infinity)
            .background(Color.gray.opacity(0.2))
        }
    }
}
```

#### Frame - Distribución Proporcional

```swift
struct HStackProportional: View {
    var body: some View {
        // Usando GeometryReader para distribución proporcional
        GeometryReader { geometry in
            HStack(spacing: 0) {
                Text("25%")
                    .frame(width: geometry.size.width * 0.25)
                    .background(Color.red)

                Text("75%")
                    .frame(width: geometry.size.width * 0.75)
                    .background(Color.blue)
            }
        }
        .frame(height: 50)

        // Distribución equitativa simplificada
        HStack(spacing: 0) {
            Text("33%")
                .frame(maxWidth: .infinity)
                .background(Color.red)
            Text("33%")
                .frame(maxWidth: .infinity)
                .background(Color.green)
            Text("33%")
                .frame(maxWidth: .infinity)
                .background(Color.blue)
        }
        .frame(height: 50)
    }
}
```

---

### Comparación Row / HStack

| Feature | Compose (Row) | SwiftUI (HStack) |
|---------|---------------|------------------|
| Uso básico | `Row { }` | `HStack { }` |
| Alineación vertical | `verticalAlignment = Alignment.CenterVertically` | `alignment: .center` |
| Espacio entre items | `horizontalArrangement = Arrangement.spacedBy(16.dp)` | `spacing: 16` |
| Llenar ancho | `Modifier.fillMaxWidth()` | `.frame(maxWidth: .infinity)` |
| Distribución proporcional | `Modifier.weight(1f)` | `.frame(maxWidth: .infinity)` o GeometryReader |

---

## 📦 Box / ZStack - Layout en Capas (Overlay)

Superpone elementos uno encima del otro.

### Jetpack Compose - Box

#### Uso Básico

```kotlin
@Composable
fun BoxExample() {
    Box {
        // Los elementos se apilan en orden (primero = fondo)
        Text("Fondo")
        Text("Medio")
        Text("Frente")
    }
}
```

#### Con Alineación

```kotlin
@Composable
fun BoxWithAlignment() {
    Box(
        modifier = Modifier
            .size(200.dp)
            .background(Color.LightGray),
        contentAlignment = Alignment.Center  // TopStart, TopCenter, Center, BottomEnd, etc.
    ) {
        Text("Centrado")
    }
}
```

#### Todas las Opciones de Alineación

```kotlin
@Composable
fun BoxAlignments() {
    Box(modifier = Modifier.size(200.dp).background(Color.LightGray)) {
        // 9 posiciones posibles
        Text("TL", modifier = Modifier.align(Alignment.TopStart))
        Text("TC", modifier = Modifier.align(Alignment.TopCenter))
        Text("TR", modifier = Modifier.align(Alignment.TopEnd))

        Text("CL", modifier = Modifier.align(Alignment.CenterStart))
        Text("C", modifier = Modifier.align(Alignment.Center))
        Text("CR", modifier = Modifier.align(Alignment.CenterEnd))

        Text("BL", modifier = Modifier.align(Alignment.BottomStart))
        Text("BC", modifier = Modifier.align(Alignment.BottomCenter))
        Text("BR", modifier = Modifier.align(Alignment.BottomEnd))
    }
}
```

#### Ejemplo: Badge en Imagen

```kotlin
@Composable
fun ImageWithBadge() {
    Box {
        // Imagen de fondo
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Avatar",
            modifier = Modifier.size(100.dp)
        )

        // Badge en la esquina superior derecha
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .size(24.dp)
                .background(Color.Red, shape = CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Text("5", color = Color.White, fontSize = 12.sp)
        }
    }
}
```

---

### SwiftUI - ZStack

#### Uso Básico

```swift
struct ZStackExample: View {
    var body: some View {
        ZStack {
            // Los elementos se apilan en orden (primero = fondo)
            Text("Fondo")
            Text("Medio")
            Text("Frente")
        }
    }
}
```

#### Con Alineación

```swift
struct ZStackWithAlignment: View {
    var body: some View {
        ZStack(alignment: .center) {  // .topLeading, .center, .bottomTrailing, etc.
            Rectangle()
                .fill(Color.gray.opacity(0.3))
                .frame(width: 200, height: 200)

            Text("Centrado")
        }
    }
}
```

#### Todas las Opciones de Alineación

```swift
struct ZStackAlignments: View {
    var body: some View {
        ZStack {
            Rectangle()
                .fill(Color.gray.opacity(0.2))
                .frame(width: 200, height: 200)

            // 9 posiciones posibles usando alignment en ZStack individual
            ZStack(alignment: .topLeading) { Text("TL") }
            ZStack(alignment: .top) { Text("TC") }
            ZStack(alignment: .topTrailing) { Text("TR") }

            ZStack(alignment: .leading) { Text("CL") }
            ZStack(alignment: .center) { Text("C") }
            ZStack(alignment: .trailing) { Text("CR") }

            ZStack(alignment: .bottomLeading) { Text("BL") }
            ZStack(alignment: .bottom) { Text("BC") }
            ZStack(alignment: .bottomTrailing) { Text("BR") }
        }
    }
}
```

#### Ejemplo: Badge en Imagen

```swift
struct ImageWithBadge: View {
    var body: some View {
        ZStack(alignment: .topTrailing) {
            // Imagen de fondo
            Circle()
                .fill(Color.gray.opacity(0.3))
                .frame(width: 100, height: 100)
                .overlay(
                    Image(systemName: "person.fill")
                        .foregroundColor(.gray)
                )

            // Badge en la esquina superior derecha
            ZStack {
                Circle()
                    .fill(Color.red)
                    .frame(width: 24, height: 24)

                Text("5")
                    .font(.caption2)
                    .foregroundColor(.white)
            }
            .offset(x: 5, y: -5)
        }
    }
}
```

---

### Comparación Box / ZStack

| Feature | Compose (Box) | SwiftUI (ZStack) |
|---------|---------------|------------------|
| Uso básico | `Box { }` | `ZStack { }` |
| Alineación general | `contentAlignment = Alignment.Center` | `alignment: .center` |
| Alineación individual | `Modifier.align(Alignment.TopEnd)` | Usar `.offset()` o nested ZStack |
| Tamaño fijo | `Modifier.size(200.dp)` | `.frame(width: 200, height: 200)` |

---

## 🎨 Ejemplo Completo: Pantalla de Login

Combinemos todos los layouts en un ejemplo real.

### Jetpack Compose

```kotlin
@Composable
fun LoginScreen() {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF6200EE), Color(0xFF3700B3))
                )
            )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // Logo
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .background(Color.White, shape = CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Lock,
                    contentDescription = "Logo",
                    tint = Color(0xFF6200EE),
                    modifier = Modifier.size(50.dp)
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Título
            Text(
                text = "Bienvenido",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            Text(
                text = "Inicia sesión para continuar",
                fontSize = 16.sp,
                color = Color.White.copy(alpha = 0.8f)
            )

            Spacer(modifier = Modifier.height(48.dp))

            // Campo email
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                leadingIcon = {
                    Icon(Icons.Default.Email, contentDescription = null)
                },
                modifier = Modifier.fillMaxWidth(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = Color.White,
                    unfocusedContainerColor = Color.White
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Campo password
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Contraseña") },
                leadingIcon = {
                    Icon(Icons.Default.Lock, contentDescription = null)
                },
                modifier = Modifier.fillMaxWidth(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = Color.White,
                    unfocusedContainerColor = Color.White
                )
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Olvidé contraseña
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.End
            ) {
                TextButton(onClick = { }) {
                    Text("¿Olvidaste tu contraseña?", color = Color.White)
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Botón Login
            Button(
                onClick = { },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.White,
                    contentColor = Color(0xFF6200EE)
                )
            ) {
                Text("INICIAR SESIÓN", fontWeight = FontWeight.Bold)
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Divider con texto
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Divider(modifier = Modifier.weight(1f), color = Color.White.copy(alpha = 0.5f))
                Text(
                    "  O  ",
                    color = Color.White.copy(alpha = 0.8f)
                )
                Divider(modifier = Modifier.weight(1f), color = Color.White.copy(alpha = 0.5f))
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Botones sociales
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Google
                OutlinedButton(
                    onClick = { },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.outlinedButtonColors(
                        containerColor = Color.White
                    )
                ) {
                    Text("Google", color = Color.Black)
                }

                // Facebook
                OutlinedButton(
                    onClick = { },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.outlinedButtonColors(
                        containerColor = Color.White
                    )
                ) {
                    Text("Facebook", color = Color.Black)
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            // Registro
            Row {
                Text("¿No tienes cuenta? ", color = Color.White.copy(alpha = 0.8f))
                TextButton(onClick = { }) {
                    Text("Regístrate", color = Color.White, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun LoginScreenPreview() {
    LoginScreen()
}
```

---

### SwiftUI

```swift
struct LoginScreen: View {
    @State private var email = ""
    @State private var password = ""

    var body: some View {
        ZStack {
            // Fondo con gradiente
            LinearGradient(
                gradient: Gradient(colors: [Color.purple, Color.purple.opacity(0.7)]),
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()

            VStack(spacing: 0) {
                Spacer()

                // Logo
                ZStack {
                    Circle()
                        .fill(Color.white)
                        .frame(width: 100, height: 100)

                    Image(systemName: "lock.fill")
                        .font(.system(size: 50))
                        .foregroundColor(.purple)
                }

                // Título
                Text("Bienvenido")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                    .padding(.top, 32)

                Text("Inicia sesión para continuar")
                    .font(.body)
                    .foregroundColor(.white.opacity(0.8))
                    .padding(.top, 4)

                // Formulario
                VStack(spacing: 16) {
                    // Campo email
                    HStack {
                        Image(systemName: "envelope")
                            .foregroundColor(.gray)
                        TextField("Email", text: $email)
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(10)

                    // Campo password
                    HStack {
                        Image(systemName: "lock")
                            .foregroundColor(.gray)
                        SecureField("Contraseña", text: $password)
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal, 32)
                .padding(.top, 48)

                // Olvidé contraseña
                HStack {
                    Spacer()
                    Button("¿Olvidaste tu contraseña?") { }
                        .font(.caption)
                        .foregroundColor(.white)
                }
                .padding(.horizontal, 32)
                .padding(.top, 8)

                // Botón Login
                Button(action: {}) {
                    Text("INICIAR SESIÓN")
                        .fontWeight(.bold)
                        .foregroundColor(.purple)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.white)
                        .cornerRadius(10)
                }
                .padding(.horizontal, 32)
                .padding(.top, 24)

                // Divider con texto
                HStack {
                    Rectangle()
                        .fill(Color.white.opacity(0.5))
                        .frame(height: 1)
                    Text("O")
                        .foregroundColor(.white.opacity(0.8))
                        .padding(.horizontal, 8)
                    Rectangle()
                        .fill(Color.white.opacity(0.5))
                        .frame(height: 1)
                }
                .padding(.horizontal, 32)
                .padding(.top, 16)

                // Botones sociales
                HStack(spacing: 16) {
                    Button(action: {}) {
                        Text("Google")
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                    }

                    Button(action: {}) {
                        Text("Facebook")
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                    }
                }
                .padding(.horizontal, 32)
                .padding(.top, 16)

                Spacer()

                // Registro
                HStack {
                    Text("¿No tienes cuenta?")
                        .foregroundColor(.white.opacity(0.8))
                    Button("Regístrate") { }
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                }
                .padding(.bottom, 32)
            }
        }
    }
}

#Preview {
    LoginScreen()
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear una pantalla de perfil de usuario combinando los 3 layouts.

### Requisitos

**Estructura:**
- Usa `Box/ZStack` para el fondo
- Usa `Column/VStack` para el contenido principal
- Usa `Row/HStack` para elementos horizontales

**Elementos a incluir:**
- Header con imagen de portada
- Avatar circular superpuesto en el header (usa Box/ZStack)
- Nombre de usuario centrado
- Bio del usuario
- Estadísticas en fila (Posts, Seguidores, Siguiendo)
- Botón "Editar Perfil"
- Grid de fotos (usa Row/HStack múltiples o avanza a la siguiente guía de Grids)

### Bonus

- Añade un gradiente de fondo
- Implementa estado para el botón de seguir
- Añade íconos a las estadísticas

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **Layouts**: [developer.android.com/jetpack/compose/layouts/basics](https://developer.android.com/jetpack/compose/layouts/basics)
- **Column**: [developer.android.com/reference/kotlin/androidx/compose/foundation/layout/package-summary#Column(androidx.compose.ui.Modifier,androidx.compose.foundation.layout.Arrangement.Vertical,androidx.compose.ui.Alignment.Horizontal,kotlin.Function1))](https://developer.android.com/reference/kotlin/androidx/compose/foundation/layout/package-summary)
- **Weight**: [developer.android.com/jetpack/compose/layouts/basics#weight](https://developer.android.com/jetpack/compose/layouts/basics#weight)

### SwiftUI
- **Stacks**: [developer.apple.com/documentation/swiftui/building-layouts-with-stack-views](https://developer.apple.com/documentation/swiftui/building-layouts-with-stack-views)
- **VStack**: [developer.apple.com/documentation/swiftui/vstack](https://developer.apple.com/documentation/swiftui/vstack)
- **Layout**: [developer.apple.com/documentation/swiftui/layout](https://developer.apple.com/documentation/swiftui/layout)

---

**Anterior:** [03_COMPONENTES_BASICOS.md](03_COMPONENTES_BASICOS.md)
**Siguiente:** [05_LISTAS_Y_GRIDS.md](05_LISTAS_Y_GRIDS.md) - Listas y grillas

