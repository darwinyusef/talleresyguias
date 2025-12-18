# ✨ Animaciones y Gestos

> **Jetpack Compose (Android) & SwiftUI (iOS) - Movimiento y Interactividad**

---

## 🎯 Objetivo

Dominar animaciones, transiciones y gestos para crear interfaces fluidas e interactivas.

---

## 📚 Conceptos Fundamentales

### Principios de Animación

| Principio | Descripción | Uso |
|-----------|-------------|-----|
| **Timing** | Duración y velocidad | Definir rapidez de la animación |
| **Easing** | Aceleración/desaceleración | Natural vs. lineal |
| **Staging** | Dirigir atención | Animar elementos importantes |
| **Follow Through** | Continuación del movimiento | Rebotes, inercia |

### Tipos de Animaciones

```
Animaciones
├── Valor Simple (tamaño, color, posición)
├── Estado (aparecer/desaparecer)
├── Contenido (cambio de datos)
└── Gestos (drag, swipe, pinch)
```

---

## 🎨 Animaciones Básicas - Valores Simples

### Jetpack Compose - animate*AsState

#### Animar Tamaño

```kotlin
@Composable
fun AnimatedSizeExample() {
    var expanded by remember { mutableStateOf(false) }

    // Animar el tamaño
    val size by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = tween(durationMillis = 300)
    )

    Box(
        modifier = Modifier
            .size(size)
            .background(Color.Blue, shape = RoundedCornerShape(16.dp))
            .clickable { expanded = !expanded },
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = if (expanded) "Click para encoger" else "Click para expandir",
            color = Color.White,
            textAlign = TextAlign.Center
        )
    }
}
```

#### Animar Color

```kotlin
@Composable
fun AnimatedColorExample() {
    var isRed by remember { mutableStateOf(true) }

    val color by animateColorAsState(
        targetValue = if (isRed) Color.Red else Color.Blue,
        animationSpec = tween(durationMillis = 500)
    )

    Box(
        modifier = Modifier
            .size(150.dp)
            .background(color, shape = CircleShape)
            .clickable { isRed = !isRed },
        contentAlignment = Alignment.Center
    ) {
        Text("Cambiar color", color = Color.White)
    }
}
```

#### Animar Múltiples Propiedades

```kotlin
@Composable
fun MultiPropertyAnimation() {
    var toggled by remember { mutableStateOf(false) }

    val size by animateDpAsState(
        targetValue = if (toggled) 200.dp else 100.dp
    )

    val color by animateColorAsState(
        targetValue = if (toggled) Color.Green else Color.Red
    )

    val rotation by animateFloatAsState(
        targetValue = if (toggled) 360f else 0f
    )

    Box(
        modifier = Modifier
            .size(size)
            .rotate(rotation)
            .background(color, shape = RoundedCornerShape(16.dp))
            .clickable { toggled = !toggled },
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = Icons.Default.Favorite,
            contentDescription = null,
            tint = Color.White,
            modifier = Modifier.size(48.dp)
        )
    }
}
```

#### Specs de Animación

```kotlin
@Composable
fun AnimationSpecsExample() {
    var started by remember { mutableStateOf(false) }
    val offset by animateDpAsState(
        targetValue = if (started) 300.dp else 0.dp,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        )
    )

    Column {
        Box(
            modifier = Modifier
                .offset(x = offset)
                .size(50.dp)
                .background(Color.Blue, shape = CircleShape)
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = { started = !started }) {
            Text("Animar")
        }

        Text("Specs disponibles:", fontWeight = FontWeight.Bold)
        Text("• tween (linear)")
        Text("• spring (con rebote)")
        Text("• repeatable (repetir N veces)")
        Text("• infiniteRepeatable (infinito)")
        Text("• snap (instantáneo)")
    }
}

// Ejemplos de specs
val tweenSpec = tween<Dp>(
    durationMillis = 300,
    easing = FastOutSlowInEasing
)

val springSpec = spring<Dp>(
    dampingRatio = Spring.DampingRatioHighBouncy,
    stiffness = Spring.StiffnessMedium
)

val repeatableSpec = repeatable<Dp>(
    iterations = 3,
    animation = tween(300),
    repeatMode = RepeatMode.Reverse
)

val infiniteSpec = infiniteRepeatable<Dp>(
    animation = tween(1000),
    repeatMode = RepeatMode.Reverse
)
```

---

### SwiftUI - Animation Modifier

#### Animar Tamaño

```swift
struct AnimatedSizeExample: View {
    @State private var expanded = false

    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(Color.blue)
            .frame(width: expanded ? 200 : 100, height: expanded ? 200 : 100)
            .animation(.easeInOut(duration: 0.3), value: expanded)
            .overlay(
                Text(expanded ? "Click para encoger" : "Click para expandir")
                    .foregroundColor(.white)
                    .multilineTextAlignment(.center)
            )
            .onTapGesture {
                expanded.toggle()
            }
    }
}
```

#### Animar Color

```swift
struct AnimatedColorExample: View {
    @State private var isRed = true

    var body: some View {
        Circle()
            .fill(isRed ? Color.red : Color.blue)
            .frame(width: 150, height: 150)
            .animation(.easeInOut(duration: 0.5), value: isRed)
            .overlay(
                Text("Cambiar color")
                    .foregroundColor(.white)
            )
            .onTapGesture {
                isRed.toggle()
            }
    }
}
```

#### Animar Múltiples Propiedades

```swift
struct MultiPropertyAnimation: View {
    @State private var toggled = false

    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(toggled ? Color.green : Color.red)
            .frame(width: toggled ? 200 : 100, height: toggled ? 200 : 100)
            .rotationEffect(.degrees(toggled ? 360 : 0))
            .animation(.easeInOut(duration: 0.5), value: toggled)
            .overlay(
                Image(systemName: "heart.fill")
                    .font(.system(size: 48))
                    .foregroundColor(.white)
            )
            .onTapGesture {
                toggled.toggle()
            }
    }
}
```

#### Tipos de Animación

```swift
struct AnimationTypesExample: View {
    @State private var started = false

    var body: some View {
        VStack(spacing: 20) {
            // Linear
            Circle()
                .fill(Color.blue)
                .frame(width: 50, height: 50)
                .offset(x: started ? 150 : 0)
                .animation(.linear(duration: 1), value: started)

            // EaseInOut
            Circle()
                .fill(Color.green)
                .frame(width: 50, height: 50)
                .offset(x: started ? 150 : 0)
                .animation(.easeInOut(duration: 1), value: started)

            // Spring
            Circle()
                .fill(Color.red)
                .frame(width: 50, height: 50)
                .offset(x: started ? 150 : 0)
                .animation(.spring(response: 0.5, dampingFraction: 0.6), value: started)

            // Spring con rebote
            Circle()
                .fill(Color.purple)
                .frame(width: 50, height: 50)
                .offset(x: started ? 150 : 0)
                .animation(.spring(response: 0.5, dampingFraction: 0.3), value: started)

            Button("Animar") {
                started.toggle()
            }
            .buttonStyle(.borderedProminent)

            VStack(alignment: .leading, spacing: 4) {
                Text("Tipos disponibles:").fontWeight(.bold)
                Text("• .linear - velocidad constante")
                Text("• .easeIn - acelera al inicio")
                Text("• .easeOut - desacelera al final")
                Text("• .easeInOut - suave inicio y fin")
                Text("• .spring - con rebote")
            }
            .font(.caption)
        }
        .padding()
    }
}
```

---

## 🎭 Transiciones de Visibilidad

### Jetpack Compose - AnimatedVisibility

```kotlin
@Composable
fun AnimatedVisibilityExample() {
    var visible by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Button(onClick = { visible = !visible }) {
            Text(if (visible) "Ocultar" else "Mostrar")
        }

        Spacer(modifier = Modifier.height(16.dp))

        AnimatedVisibility(
            visible = visible,
            enter = fadeIn() + slideInVertically(),
            exit = fadeOut() + slideOutVertically()
        ) {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.Blue)
            ) {
                Text(
                    text = "¡Contenido animado!",
                    modifier = Modifier.padding(32.dp),
                    color = Color.White,
                    style = MaterialTheme.typography.headlineSmall
                )
            }
        }
    }
}
```

#### Tipos de Transiciones

```kotlin
@Composable
fun TransitionTypesExample() {
    var selectedTransition by remember { mutableStateOf(0) }
    var visible by remember { mutableStateOf(true) }

    val transitions = listOf(
        "Fade" to (fadeIn() to fadeOut()),
        "Slide Horizontal" to (slideInHorizontally() to slideOutHorizontally()),
        "Slide Vertical" to (slideInVertically() to slideOutVertically()),
        "Scale" to (scaleIn() to scaleOut()),
        "Expand" to (expandIn() to shrinkOut())
    )

    Column(modifier = Modifier.padding(16.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Button(onClick = { visible = !visible }) {
                Text(if (visible) "Ocultar" else "Mostrar")
            }

            Button(onClick = {
                selectedTransition = (selectedTransition + 1) % transitions.size
            }) {
                Text("Cambiar tipo")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            "Transición actual: ${transitions[selectedTransition].first}",
            style = MaterialTheme.typography.titleMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        AnimatedVisibility(
            visible = visible,
            enter = transitions[selectedTransition].second.first,
            exit = transitions[selectedTransition].second.second
        ) {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = Color.Green)
            ) {
                Column(modifier = Modifier.padding(24.dp)) {
                    Icon(
                        imageVector = Icons.Default.CheckCircle,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(48.dp)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "Contenido animado",
                        color = Color.White,
                        style = MaterialTheme.typography.titleLarge
                    )
                }
            }
        }
    }
}
```

---

### SwiftUI - Transition

```swift
struct AnimatedVisibilityExample: View {
    @State private var visible = true

    var body: some View {
        VStack(spacing: 16) {
            Button(visible ? "Ocultar" : "Mostrar") {
                withAnimation {
                    visible.toggle()
                }
            }
            .buttonStyle(.borderedProminent)

            if visible {
                RoundedRectangle(cornerRadius: 16)
                    .fill(Color.blue)
                    .frame(height: 150)
                    .overlay(
                        Text("¡Contenido animado!")
                            .font(.title)
                            .foregroundColor(.white)
                    )
                    .transition(.opacity.combined(with: .slide))
            }
        }
        .padding()
    }
}
```

#### Tipos de Transiciones

```swift
struct TransitionTypesExample: View {
    @State private var visible = true
    @State private var selectedTransition = 0

    let transitions: [(String, AnyTransition)] = [
        ("Fade", .opacity),
        ("Scale", .scale),
        ("Slide", .slide),
        ("Move (Edge)", .move(edge: .bottom)),
        ("Scale + Fade", .scale.combined(with: .opacity)),
        ("Asymmetric", .asymmetric(
            insertion: .move(edge: .leading),
            removal: .move(edge: .trailing)
        ))
    ]

    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Button(visible ? "Ocultar" : "Mostrar") {
                    withAnimation {
                        visible.toggle()
                    }
                }

                Button("Cambiar tipo") {
                    selectedTransition = (selectedTransition + 1) % transitions.count
                }
            }
            .buttonStyle(.bordered)

            Text("Transición: \(transitions[selectedTransition].0)")
                .font(.headline)

            if visible {
                RoundedRectangle(cornerRadius: 16)
                    .fill(Color.green)
                    .frame(width: 200, height: 150)
                    .overlay(
                        VStack {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.system(size: 48))
                                .foregroundColor(.white)
                            Text("Contenido animado")
                                .foregroundColor(.white)
                        }
                    )
                    .transition(transitions[selectedTransition].1)
            }
        }
        .padding()
    }
}
```

---

## 🎬 Animaciones de Contenido

### Jetpack Compose - AnimatedContent

```kotlin
@Composable
fun AnimatedContentExample() {
    var count by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        AnimatedContent(
            targetState = count,
            transitionSpec = {
                slideInVertically { height -> height } + fadeIn() togetherWith
                slideOutVertically { height -> -height } + fadeOut()
            },
            label = "count animation"
        ) { targetCount ->
            Text(
                text = targetCount.toString(),
                style = MaterialTheme.typography.displayLarge,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(32.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
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

#### Lista Animada

```kotlin
@Composable
fun AnimatedListExample() {
    var items by remember {
        mutableStateOf((1..5).map { "Item $it" })
    }

    Column(modifier = Modifier.padding(16.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Button(onClick = {
                items = items + "Item ${items.size + 1}"
            }) {
                Text("Añadir")
            }

            Button(
                onClick = { if (items.isNotEmpty()) items = items.dropLast(1) },
                enabled = items.isNotEmpty()
            ) {
                Text("Eliminar")
            }

            Button(onClick = { items = items.shuffled() }) {
                Text("Mezclar")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(
                items = items,
                key = { it }
            ) { item ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .animateItemPlacement(
                            animationSpec = spring(
                                dampingRatio = Spring.DampingRatioMediumBouncy,
                                stiffness = Spring.StiffnessLow
                            )
                        ),
                    colors = CardDefaults.cardColors(
                        containerColor = Color(Random.nextInt(256), Random.nextInt(256), Random.nextInt(256))
                    )
                ) {
                    Text(
                        text = item,
                        modifier = Modifier.padding(16.dp),
                        color = Color.White,
                        style = MaterialTheme.typography.titleMedium
                    )
                }
            }
        }
    }
}
```

---

### SwiftUI - ContentTransition

```swift
struct AnimatedContentExample: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 32) {
            Text("\(count)")
                .font(.system(size: 80, weight: .bold))
                .contentTransition(.numericText())
                .animation(.spring(), value: count)

            HStack(spacing: 16) {
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

#### Lista Animada

```swift
struct AnimatedListExample: View {
    @State private var items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

    var body: some View {
        VStack {
            HStack(spacing: 8) {
                Button("Añadir") {
                    withAnimation {
                        items.append("Item \(items.count + 1)")
                    }
                }

                Button("Eliminar") {
                    withAnimation {
                        if !items.isEmpty {
                            items.removeLast()
                        }
                    }
                }
                .disabled(items.isEmpty)

                Button("Mezclar") {
                    withAnimation {
                        items.shuffle()
                    }
                }
            }
            .buttonStyle(.bordered)

            List {
                ForEach(items, id: \.self) { item in
                    HStack {
                        Text(item)
                            .font(.headline)
                        Spacer()
                    }
                    .padding()
                    .background(
                        Color(
                            red: .random(in: 0...1),
                            green: .random(in: 0...1),
                            blue: .random(in: 0...1)
                        )
                    )
                    .cornerRadius(8)
                    .foregroundColor(.white)
                }
                .onMove { from, to in
                    withAnimation {
                        items.move(fromOffsets: from, toOffset: to)
                    }
                }
                .onDelete { indexSet in
                    withAnimation {
                        items.remove(atOffsets: indexSet)
                    }
                }
            }
            .listStyle(.plain)
        }
        .padding()
    }
}
```

---

## 👆 Gestos y Arrastrar

### Jetpack Compose - Gestos

```kotlin
@Composable
fun DraggableExample() {
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Box(
            modifier = Modifier
                .offset { IntOffset(offsetX.roundToInt(), offsetY.roundToInt()) }
                .size(100.dp)
                .background(Color.Blue, shape = CircleShape)
                .pointerInput(Unit) {
                    detectDragGestures { change, dragAmount ->
                        change.consume()
                        offsetX += dragAmount.x
                        offsetY += dragAmount.y
                    }
                },
            contentAlignment = Alignment.Center
        ) {
            Text("Arrástra me", color = Color.White, textAlign = TextAlign.Center)
        }
    }
}
```

#### Swipe to Dismiss

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SwipeToDismissExample() {
    var items by remember {
        mutableStateOf((1..10).map { "Item $it" })
    }

    LazyColumn {
        items(
            items = items,
            key = { it }
        ) { item ->
            val dismissState = rememberDismissState(
                confirmValueChange = {
                    if (it == DismissValue.DismissedToEnd || it == DismissValue.DismissedToStart) {
                        items = items.filter { i -> i != item }
                        true
                    } else {
                        false
                    }
                }
            )

            SwipeToDismiss(
                state = dismissState,
                background = {
                    val color = when (dismissState.dismissDirection) {
                        DismissDirection.StartToEnd -> Color.Green
                        DismissDirection.EndToStart -> Color.Red
                        null -> Color.Transparent
                    }

                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(color)
                            .padding(16.dp),
                        contentAlignment = if (dismissState.dismissDirection == DismissDirection.StartToEnd) {
                            Alignment.CenterStart
                        } else {
                            Alignment.CenterEnd
                        }
                    ) {
                        Icon(
                            imageVector = if (dismissState.dismissDirection == DismissDirection.StartToEnd) {
                                Icons.Default.Check
                            } else {
                                Icons.Default.Delete
                            },
                            contentDescription = null,
                            tint = Color.White
                        )
                    }
                },
                dismissContent = {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                    ) {
                        Text(
                            text = item,
                            modifier = Modifier.padding(16.dp),
                            style = MaterialTheme.typography.titleMedium
                        )
                    }
                }
            )
        }
    }
}
```

---

### SwiftUI - Gestos

```swift
struct DraggableExample: View {
    @State private var offset = CGSize.zero

    var body: some View {
        Circle()
            .fill(Color.blue)
            .frame(width: 100, height: 100)
            .offset(offset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                    }
                    .onEnded { _ in
                        withAnimation(.spring()) {
                            offset = .zero
                        }
                    }
            )
            .overlay(
                Text("Arrástra me")
                    .foregroundColor(.white)
            )
    }
}
```

#### Swipe to Delete

```swift
struct SwipeToDeleteExample: View {
    @State private var items = (1...10).map { "Item \($0)" }

    var body: some View {
        List {
            ForEach(items, id: \.self) { item in
                Text(item)
                    .font(.headline)
                    .padding(.vertical, 8)
            }
            .onDelete { indexSet in
                items.remove(atOffsets: indexSet)
            }
        }
        .listStyle(.plain)
    }
}
```

#### Gestos Avanzados

```swift
struct AdvancedGesturesExample: View {
    @State private var scale: CGFloat = 1.0
    @State private var rotation: Angle = .zero
    @State private var offset = CGSize.zero

    var body: some View {
        VStack {
            Text("Usa gestos:")
                .font(.headline)
            Text("• Drag para mover")
            Text("• Pinch para escalar")
            Text("• Rotate para rotar")
                .padding()

            RoundedRectangle(cornerRadius: 16)
                .fill(
                    LinearGradient(
                        colors: [.blue, .purple],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: 150, height: 150)
                .scaleEffect(scale)
                .rotationEffect(rotation)
                .offset(offset)
                .gesture(
                    SimultaneousGesture(
                        DragGesture()
                            .onChanged { value in
                                offset = value.translation
                            },
                        MagnificationGesture()
                            .onChanged { value in
                                scale = value
                            }
                    )
                    .simultaneously(with:
                        RotationGesture()
                            .onChanged { value in
                                rotation = value
                            }
                    )
                )
                .gesture(
                    TapGesture(count: 2)
                        .onEnded {
                            withAnimation(.spring()) {
                                scale = 1.0
                                rotation = .zero
                                offset = .zero
                            }
                        }
                )
                .overlay(
                    Text("Doble tap para reset")
                        .foregroundColor(.white)
                        .font(.caption)
                )
        }
    }
}
```

---

## 🎪 Ejemplo Completo: Like Button Animado

### Jetpack Compose

```kotlin
@Composable
fun AnimatedLikeButton() {
    var isLiked by remember { mutableStateOf(false) }
    var showParticles by remember { mutableStateOf(false) }

    val scale by animateFloatAsState(
        targetValue = if (isLiked) 1.2f else 1f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        )
    )

    val color by animateColorAsState(
        targetValue = if (isLiked) Color.Red else Color.Gray,
        animationSpec = tween(durationMillis = 300)
    )

    Box(
        modifier = Modifier
            .size(100.dp)
            .clickable {
                isLiked = !isLiked
                if (isLiked) showParticles = true
            },
        contentAlignment = Alignment.Center
    ) {
        // Particles effect
        if (showParticles) {
            LaunchedEffect(Unit) {
                kotlinx.coroutines.delay(500)
                showParticles = false
            }

            repeat(8) { index ->
                val angle = (360f / 8f) * index
                val offsetX by animateDpAsState(
                    targetValue = if (showParticles) 40.dp else 0.dp,
                    animationSpec = tween(durationMillis = 500)
                )

                Box(
                    modifier = Modifier
                        .offset(
                            x = offsetX * cos(Math.toRadians(angle.toDouble())).toFloat(),
                            y = offsetX * sin(Math.toRadians(angle.toDouble())).toFloat()
                        )
                        .size(8.dp)
                        .background(Color.Red, shape = CircleShape)
                )
            }
        }

        // Heart icon
        Icon(
            imageVector = if (isLiked) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
            contentDescription = "Like",
            tint = color,
            modifier = Modifier
                .size(48.dp)
                .scale(scale)
        )
    }
}
```

---

### SwiftUI

```swift
struct AnimatedLikeButton: View {
    @State private var isLiked = false
    @State private var showParticles = false
    @State private var scale: CGFloat = 1.0

    var body: some View {
        ZStack {
            // Particles
            if showParticles {
                ForEach(0..<8) { index in
                    Circle()
                        .fill(Color.red)
                        .frame(width: 8, height: 8)
                        .offset(
                            x: showParticles ? cos(Double(index) * .pi / 4) * 40 : 0,
                            y: showParticles ? sin(Double(index) * .pi / 4) * 40 : 0
                        )
                        .opacity(showParticles ? 0 : 1)
                }
            }

            // Heart icon
            Image(systemName: isLiked ? "heart.fill" : "heart")
                .font(.system(size: 48))
                .foregroundColor(isLiked ? .red : .gray)
                .scaleEffect(scale)
        }
        .frame(width: 100, height: 100)
        .onTapGesture {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                isLiked.toggle()
                scale = isLiked ? 1.2 : 1.0
            }

            if isLiked {
                withAnimation(.easeOut(duration: 0.5)) {
                    showParticles = true
                }

                DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                    showParticles = false
                }
            }
        }
    }
}
```

---

## 📝 Ejercicio Práctico

### Objetivo

Crear un carrusel de imágenes con gestos y animaciones.

### Requisitos

- Swipe horizontal para cambiar de imagen
- Animación de transición entre imágenes
- Indicadores de página (dots)
- Zoom con pinch gesture (bonus)
- Autoplay con timer (bonus)

---

## 🔗 Recursos Adicionales

### Jetpack Compose
- **Animations**: [developer.android.com/jetpack/compose/animation](https://developer.android.com/jetpack/compose/animation)
- **Gestures**: [developer.android.com/jetpack/compose/gestures](https://developer.android.com/jetpack/compose/gestures)

### SwiftUI
- **Animations**: [developer.apple.com/documentation/swiftui/animation](https://developer.apple.com/documentation/swiftui/animation)
- **Gestures**: [developer.apple.com/documentation/swiftui/gestures](https://developer.apple.com/documentation/swiftui/gestures)

---

**Anterior:** [08_POC_LOGICA_NEGOCIO.md](08_POC_LOGICA_NEGOCIO.md)
**Siguiente:** [10_TEMAS_DARK_MODE.md](10_TEMAS_DARK_MODE.md) - Temas y personalización

