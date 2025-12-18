# 🛠️ Setup del Ambiente de Desarrollo

> **Jetpack Compose (Android) & SwiftUI (iOS) - Configuración Inicial**

---

## 🎯 Objetivo

Configurar el ambiente de desarrollo para poder crear aplicaciones móviles con Jetpack Compose y SwiftUI.

---

## 📱 Android - Jetpack Compose

### Requisitos del Sistema

| Componente | Requisito Mínimo | Recomendado |
|------------|------------------|-------------|
| **OS** | Windows 10+, macOS 10.14+, Linux | macOS Sonoma, Windows 11 |
| **RAM** | 8 GB | 16 GB o más |
| **Disco** | 4 GB de espacio libre | SSD con 10 GB+ |
| **Procesador** | x86_64 CPU | Intel i5/i7, Apple Silicon |

### 1. Instalar Android Studio

#### Descargar

1. Ve a [developer.android.com/studio](https://developer.android.com/studio)
2. Descarga la versión estable más reciente (Giraffe o superior)
3. Instala siguiendo las instrucciones del instalador

#### Primer Inicio

Al abrir Android Studio por primera vez:

```
1. Welcome Screen → Next
2. Standard Installation → Next
3. Selecciona tema (Light/Dark) → Next
4. Verify Settings → Finish
5. Espera a que descargue SDK y componentes (~2-3 GB)
```

### 2. Verificar Instalación

#### SDK Manager

```
Android Studio → Settings (⌘ + , en Mac / Ctrl + Alt + S en Windows)
  → Appearance & Behavior
  → System Settings
  → Android SDK
```

Verifica que estén instalados:
- ✅ **Android SDK Platform 34** (Android 14)
- ✅ **Android SDK Build-Tools 34**
- ✅ **Android Emulator**
- ✅ **Android SDK Platform-Tools**

### 3. Crear Primer Proyecto Compose

#### Paso a Paso

```
1. Android Studio → New Project
2. Selecciona: "Empty Activity" (con logo de Jetpack Compose)
3. Configura:
   - Name: HelloCompose
   - Package name: com.example.hellocompose
   - Save location: [tu carpeta de proyectos]
   - Language: Kotlin
   - Minimum SDK: API 24 (Android 7.0) - Recomendado
4. Finish
```

#### Estructura del Proyecto

```
HelloCompose/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/example/hellocompose/
│   │       │   └── MainActivity.kt          # ← Aquí escribes tu UI
│   │       └── AndroidManifest.xml
│   ├── build.gradle.kts                     # ← Dependencias
│   └── ...
├── gradle/
└── build.gradle.kts
```

#### MainActivity.kt (generado automáticamente)

```kotlin
package com.example.hellocompose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.hellocompose.ui.theme.HelloComposeTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            HelloComposeTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting("Android")
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    HelloComposeTheme {
        Greeting("Android")
    }
}
```

### 4. Configurar Emulador

#### Crear AVD (Android Virtual Device)

```
Android Studio → Device Manager (ícono de celular en toolbar)
  → Create Device
  → Selecciona: Pixel 6 (recomendado)
  → System Image: API 34 (Android 14) - Download si es necesario
  → AVD Name: Pixel_6_API_34
  → Finish
```

#### Ejecutar App

```
1. Click en el botón ▶ (Run) o Shift + F10
2. Selecciona tu emulador
3. Espera a que arranque el emulador (~30 seg primera vez)
4. La app se instalará y abrirá automáticamente
```

Deberías ver: **"Hello Android!"**

### 5. Preview en Compose

Una de las mejores features de Compose es el **Preview en tiempo real**.

#### Habilitar Preview

```kotlin
@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    HelloComposeTheme {
        Greeting("Android")
    }
}
```

El preview aparece a la derecha del código. Si no lo ves:

```
View → Tool Windows → Split (o click en "Split" arriba a la derecha)
```

#### Modificar y Ver Cambios

Cambia el código:

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "¡Hola $name! 👋",
        modifier = modifier,
        fontSize = 24.sp,
        color = Color.Blue
    )
}
```

El preview se actualiza automáticamente. **¡No necesitas ejecutar la app!**

### 6. Verificar Dependencias

Abre `app/build.gradle.kts`:

```kotlin
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")

    // Compose BOM (Bill of Materials) - versión centralizada
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")

    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

---

## 🍎 iOS - SwiftUI

### Requisitos del Sistema

| Componente | Requisito Mínimo | Recomendado |
|------------|------------------|-------------|
| **OS** | macOS Ventura 13+ | macOS Sonoma 14+ |
| **RAM** | 8 GB | 16 GB o más |
| **Disco** | 10 GB de espacio libre | 20 GB+ |
| **Procesador** | Intel o Apple Silicon | Apple Silicon (M1/M2/M3) |

**⚠️ IMPORTANTE:** SwiftUI solo se puede desarrollar en macOS con Xcode.

### 1. Instalar Xcode

#### Opción A: App Store (Recomendado)

```
1. Abre App Store
2. Busca "Xcode"
3. Click en "Get" o "Download" (~15 GB, toma tiempo)
4. Una vez instalado, abre Xcode
5. Acepta los términos y condiciones
6. Xcode instalará componentes adicionales
```

#### Opción B: Apple Developer

```
1. Ve a developer.apple.com/download
2. Busca Xcode 15+
3. Descarga el archivo .xip
4. Descomprime y mueve Xcode.app a /Applications
```

### 2. Configurar Xcode

#### Primer Inicio

```
1. Abre Xcode
2. "Install additional required components" → Install
3. Ingresa tu contraseña de macOS
4. Espera a que termine la instalación
```

#### Command Line Tools

```bash
# En Terminal:
xcode-select --install
```

Esto instala herramientas de línea de comandos necesarias.

### 3. Crear Primer Proyecto SwiftUI

#### Paso a Paso

```
1. Xcode → Create New Project
2. iOS → App → Next
3. Configura:
   - Product Name: HelloSwiftUI
   - Team: None (o tu cuenta de Apple Developer)
   - Organization Identifier: com.example
   - Bundle Identifier: com.example.HelloSwiftUI (auto-generado)
   - Interface: SwiftUI ← ¡IMPORTANTE!
   - Language: Swift
   - Storage: None
   - Include Tests: ✓ (opcional)
4. Next → Choose location → Create
```

#### Estructura del Proyecto

```
HelloSwiftUI/
├── HelloSwiftUI/
│   ├── HelloSwiftUIApp.swift           # ← Entry point
│   ├── ContentView.swift               # ← Aquí escribes tu UI
│   ├── Assets.xcassets/                # ← Imágenes, colores
│   └── Preview Content/
│       └── Preview Assets.xcassets/
└── HelloSwiftUI.xcodeproj
```

#### ContentView.swift (generado automáticamente)

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
```

### 4. Configurar Simulador

#### Seleccionar Dispositivo

En el toolbar superior:

```
Click en el menú de dispositivos (junto al botón ▶)
→ Selecciona "iPhone 15 Pro" (recomendado)
```

#### Ejecutar App

```
1. Click en el botón ▶ (Run) o ⌘ + R
2. El simulador se abrirá (~20 seg primera vez)
3. La app se instalará y abrirá automáticamente
```

Deberías ver: Un globo terráqueo 🌐 y **"Hello, world!"**

### 5. Preview en SwiftUI

SwiftUI tiene **Canvas Preview** en tiempo real.

#### Habilitar Canvas

Si no ves el preview a la derecha:

```
Editor → Canvas (o Option + ⌘ + Return)
```

#### Modificar y Ver Cambios

Cambia el código:

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "star.fill")
                .imageScale(.large)
                .foregroundStyle(.yellow)
            Text("¡Hola SwiftUI! 👋")
                .font(.title)
                .foregroundColor(.blue)
        }
        .padding()
    }
}
```

El canvas se actualiza automáticamente. **¡No necesitas ejecutar la app!**

Si no se actualiza automáticamente:

```
Click en "Resume" arriba del canvas
```

### 6. Crear Múltiples Previews

Puedes tener múltiples previews con diferentes configuraciones:

```swift
#Preview("Light Mode") {
    ContentView()
}

#Preview("Dark Mode") {
    ContentView()
        .preferredColorScheme(.dark)
}

#Preview("iPhone SE") {
    ContentView()
        .previewDevice("iPhone SE (3rd generation)")
}
```

---

## 🎨 Primer Ejemplo: Hello World Personalizado

### Jetpack Compose

```kotlin
@Composable
fun HelloWorld() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF1E88E5))
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "👋",
            fontSize = 72.sp
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "¡Hola Mundo!",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Bienvenido a Jetpack Compose",
            fontSize = 16.sp,
            color = Color.White.copy(alpha = 0.8f)
        )
    }
}

@Preview(showBackground = true)
@Composable
fun HelloWorldPreview() {
    HelloWorld()
}
```

### SwiftUI

```swift
struct HelloWorld: View {
    var body: some View {
        ZStack {
            Color(red: 0.12, green: 0.53, blue: 0.90)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                Text("👋")
                    .font(.system(size: 72))

                Text("¡Hola Mundo!")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(.white)

                Text("Bienvenido a SwiftUI")
                    .font(.body)
                    .foregroundColor(.white.opacity(0.8))
            }
            .padding(32)
        }
    }
}

#Preview {
    HelloWorld()
}
```

**Resultado:** Ambas apps se verán idénticas - fondo azul, emoji de saludo, texto centrado.

---

## 🔧 Herramientas Útiles

### Android Studio

#### Plugins Recomendados

```
Settings → Plugins → Marketplace → Buscar:
```

- **Jetpack Compose Preview** (incluido)
- **Rainbow Brackets** - Colorea los paréntesis
- **GitToolBox** - Git mejorado
- **Key Promoter X** - Aprende shortcuts

#### Shortcuts Esenciales

| Acción | Mac | Windows/Linux |
|--------|-----|---------------|
| Ejecutar app | `⌘ + R` | `Shift + F10` |
| Preview refresh | Automático | Automático |
| Buscar archivo | `⌘ + Shift + O` | `Ctrl + Shift + N` |
| Autocompletar | `⌃ + Space` | `Ctrl + Space` |
| Reformatear código | `⌘ + Option + L` | `Ctrl + Alt + L` |

### Xcode

#### Organizar Ventanas

```
Editor → Canvas                     # Preview panel
View → Navigators → Project         # File browser
View → Inspectors → Attributes      # Properties panel
```

#### Shortcuts Esenciales

| Acción | Mac |
|--------|-----|
| Ejecutar app | `⌘ + R` |
| Stop app | `⌘ + .` |
| Toggle Canvas | `Option + ⌘ + Return` |
| Resume Preview | `Option + ⌘ + P` |
| Buscar archivo | `⌘ + Shift + O` |
| Autocompletar | `Esc` o comenzar a escribir |
| Reformatear código | `⌃ + I` |

---

## 🐛 Troubleshooting

### Android Studio

#### Problema: Emulador no arranca

```bash
# Verificar virtualización:
# Windows: Habilitar Hyper-V o HAXM
# Mac: Habilitar "Rosetta" para Apple Silicon

# Reiniciar ADB:
adb kill-server
adb start-server
```

#### Problema: Build falla con error de SDK

```
Tools → SDK Manager → SDK Tools
→ Instalar "Android SDK Build-Tools"
→ Apply → OK
```

#### Problema: Preview no aparece

```
1. Build → Clean Project
2. Build → Rebuild Project
3. Invalide Caches → Invalidate and Restart
```

### Xcode

#### Problema: Simulador no arranca

```bash
# Desde Terminal:
xcrun simctl shutdown all
xcrun simctl erase all

# Luego reinicia Xcode
```

#### Problema: Canvas no actualiza

```
1. Click en "Resume" en el canvas
2. Product → Clean Build Folder (⌘ + Shift + K)
3. Cierra y reabre el archivo
```

#### Problema: "Failed to build module"

```
1. Product → Clean Build Folder
2. Cierra Xcode
3. Borra DerivedData:
   ~/Library/Developer/Xcode/DerivedData
4. Reabre el proyecto
```

---

## ✅ Verificación del Setup

### Checklist Android

- [ ] Android Studio instalado y actualizado
- [ ] SDK Platform 34 descargado
- [ ] Emulador creado y funcionando
- [ ] Proyecto HelloCompose crea y ejecuta
- [ ] Preview funciona y se actualiza
- [ ] Texto "Hello Android!" visible en emulador

### Checklist iOS

- [ ] Xcode instalado y actualizado
- [ ] Command Line Tools instalado
- [ ] Simulador iPhone 15 Pro funciona
- [ ] Proyecto HelloSwiftUI crea y ejecuta
- [ ] Canvas Preview funciona
- [ ] Texto "Hello, world!" visible en simulador

---

## 📝 Ejercicio Práctico

### Objetivo

Modificar los proyectos iniciales para personalizar el mensaje de bienvenida.

### Android (Jetpack Compose)

Modifica `Greeting` para mostrar:
- Tu nombre
- Un emoji
- Cambiar el color del texto a azul
- Aumentar el tamaño de fuente a 24sp

### iOS (SwiftUI)

Modifica `ContentView` para mostrar:
- Tu nombre
- Un emoji diferente
- Cambiar el color del texto a azul
- Aumentar el tamaño de fuente a `.title`

### Bonus

Añade un segundo `Text` debajo con un subtítulo (ej: "Aprendiendo UI declarativa").

---

## 🔗 Recursos Adicionales

### Android
- **Setup oficial**: [developer.android.com/studio/install](https://developer.android.com/studio/install)
- **Compose tutorial**: [developer.android.com/jetpack/compose/tutorial](https://developer.android.com/jetpack/compose/tutorial)
- **Emulator setup**: [developer.android.com/studio/run/emulator](https://developer.android.com/studio/run/emulator)

### iOS
- **Xcode setup**: [developer.apple.com/xcode/](https://developer.apple.com/xcode/)
- **SwiftUI tutorial**: [developer.apple.com/tutorials/swiftui](https://developer.apple.com/tutorials/swiftui)
- **Simulator guide**: [developer.apple.com/documentation/xcode/running-your-app-in-simulator-or-on-a-device](https://developer.apple.com/documentation/xcode/running-your-app-in-simulator-or-on-a-device)

---

**Anterior:** [01_INTRODUCCION_UI_DECLARATIVA.md](01_INTRODUCCION_UI_DECLARATIVA.md)
**Siguiente:** [03_COMPONENTES_BASICOS.md](03_COMPONENTES_BASICOS.md) - Componentes básicos de UI

