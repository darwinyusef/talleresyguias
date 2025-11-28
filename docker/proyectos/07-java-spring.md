# Proyecto 7: Backend con Java (Spring Boot)

## Objetivo
Crear una API REST con Spring Boot y desplegarla usando Docker.

## Prerrequisitos
- Proyectos anteriores completados
- Java 17+ instalado
- Maven o Gradle
- Conocimientos básicos de Java y Spring Boot

---

## Paso 1: Crear Proyecto Spring Boot

**Opción 1: Usando Spring Initializr (Web)**
1. Ir a https://start.spring.io/
2. Configuración:
   - Project: Maven
   - Language: Java
   - Spring Boot: 3.2.x (última estable)
   - Group: com.ejemplo
   - Artifact: api-spring
   - Packaging: Jar
   - Java: 17
3. Dependencias:
   - Spring Web
   - Spring Data JPA
   - PostgreSQL Driver
   - Lombok
   - Spring Boot DevTools
4. Descargar y extraer

**Opción 2: Usando Spring Boot CLI**
```bash
spring init \
  --dependencies=web,data-jpa,postgresql,lombok,devtools \
  --build=maven \
  --java-version=17 \
  --group-id=com.ejemplo \
  --artifact-id=api-spring \
  --name=ApiSpring \
  api-spring
```

**Opción 3: Maven directo**
```bash
mkdir -p ~/curso-docker/proyectos/07-java-spring
cd ~/curso-docker/proyectos/07-java-spring
```

## Paso 2: Estructura del Proyecto

```
07-java-spring/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── ejemplo/
│   │   │           └── apispring/
│   │   │               ├── ApiSpringApplication.java
│   │   │               ├── controller/
│   │   │               │   └── UserController.java
│   │   │               ├── model/
│   │   │               │   └── User.java
│   │   │               ├── repository/
│   │   │               │   └── UserRepository.java
│   │   │               ├── service/
│   │   │               │   └── UserService.java
│   │   │               └── dto/
│   │   │                   └── UserDTO.java
│   │   └── resources/
│   │       ├── application.properties
│   │       └── application-docker.properties
│   └── test/
├── target/           (generado después del build)
├── pom.xml
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
└── .dockerignore
```

## Paso 3: Configurar pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>com.ejemplo</groupId>
    <artifactId>api-spring</artifactId>
    <version>1.0.0</version>
    <name>ApiSpring</name>
    <description>API REST con Spring Boot</description>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- PostgreSQL -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- Validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- DevTools (solo desarrollo) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>

        <!-- Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

## Paso 4: Configurar application.properties

**src/main/resources/application.properties:**
```properties
# Server
server.port=8080
spring.application.name=api-spring

# Database
spring.datasource.url=jdbc:postgresql://localhost:5432/springdb
spring.datasource.username=usuario
spring.datasource.password=password
spring.datasource.driver-class-name=org.postgresql.Driver

# JPA
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.properties.hibernate.format_sql=true

# Logging
logging.level.org.springframework.web=INFO
logging.level.org.hibernate=INFO
logging.level.com.ejemplo=DEBUG
```

**src/main/resources/application-docker.properties:**
```properties
spring.datasource.url=jdbc:postgresql://db:5432/springdb
spring.datasource.username=usuario
spring.datasource.password=password
```

## Paso 5: Crear Modelo y Repositorio

**src/main/java/com/ejemplo/apispring/model/User.java:**
```java
package com.ejemplo.apispring.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Name is required")
    @Column(nullable = false)
    private String name;

    @Email(message = "Email should be valid")
    @NotBlank(message = "Email is required")
    @Column(nullable = false, unique = true)
    private String email;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

**src/main/java/com/ejemplo/apispring/repository/UserRepository.java:**
```java
package com.ejemplo.apispring.repository;

import com.ejemplo.apispring.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}
```

## Paso 6: Crear Servicio y Controlador

**src/main/java/com/ejemplo/apispring/service/UserService.java:**
```java
package com.ejemplo.apispring.service;

import com.ejemplo.apispring.model.User;
import com.ejemplo.apispring.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Transactional
    public User createUser(User user) {
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new RuntimeException("Email already exists");
        }
        return userRepository.save(user);
    }

    @Transactional
    public User updateUser(Long id, User userDetails) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));

        user.setName(userDetails.getName());
        user.setEmail(userDetails.getEmail());

        return userRepository.save(user);
    }

    @Transactional
    public void deleteUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));
        userRepository.delete(user);
    }
}
```

**src/main/java/com/ejemplo/apispring/controller/UserController.java:**
```java
package com.ejemplo.apispring.controller;

import com.ejemplo.apispring.model.User;
import com.ejemplo.apispring.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = userService.getAllUsers();
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userService.getUserById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
        try {
            User createdUser = userService.createUser(user);
            return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody User userDetails) {
        try {
            User updatedUser = userService.updateUser(id, userDetails);
            return ResponseEntity.ok(updatedUser);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deleteUser(@PathVariable Long id) {
        try {
            userService.deleteUser(id);
            return ResponseEntity.ok(Map.of("message", "User deleted successfully"));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
```

**Health endpoint:**
```java
package com.ejemplo.apispring.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HealthController {

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "healthy"));
    }

    @GetMapping("/")
    public ResponseEntity<Map<String, Object>> root() {
        return ResponseEntity.ok(Map.of(
            "message", "API Spring Boot",
            "version", "1.0.0",
            "status", "running"
        ));
    }
}
```

## Paso 7: Dockerfile Multi-Stage

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copiar pom.xml y descargar dependencias
COPY pom.xml .
RUN mvn dependency:go-offline

# Copiar código fuente y compilar
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Production
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copiar JAR desde stage builder
COPY --from=builder /app/target/*.jar app.jar

# Exponer puerto
EXPOSE 8080

# Usuario no-root
RUN addgroup -g 1001 -S spring && adduser -S spring -u 1001
USER spring

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/health || exit 1

# Variables de entorno
ENV SPRING_PROFILES_ACTIVE=docker

# Comando de inicio
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Paso 8: Dockerfile.dev

```dockerfile
FROM maven:3.9-eclipse-temurin-17

WORKDIR /app

# Copiar pom.xml
COPY pom.xml .
RUN mvn dependency:go-offline

# El código se monta como volumen

EXPOSE 8080

# Modo desarrollo con Spring DevTools
CMD ["mvn", "spring-boot:run"]
```

## Paso 9: Crear .dockerignore

```
target/
.mvn/
mvnw
mvnw.cmd
.git/
.gitignore
README.md
.DS_Store
*.log
.idea/
.vscode/
*.iml
```

## Paso 10: Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: springdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U usuario"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Producción
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    container_name: spring-api-prod
    restart: unless-stopped
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/springdb
      - SPRING_DATASOURCE_USERNAME=usuario
      - SPRING_DATASOURCE_PASSWORD=password
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    profiles:
      - production

  # Desarrollo
  api-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    volumes:
      - ./src:/app/src
      - ./pom.xml:/app/pom.xml
      - maven_cache:/root/.m2
    container_name: spring-api-dev
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/springdb
      - SPRING_DATASOURCE_USERNAME=usuario
      - SPRING_DATASOURCE_PASSWORD=password
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    profiles:
      - development

volumes:
  postgres_data:
  maven_cache:

networks:
  app-network:
    driver: bridge
```

## Paso 11: Construir y Ejecutar

**Desarrollo local (sin Docker):**
```bash
./mvnw spring-boot:run
```

**Producción con Docker:**
```bash
# Build
docker build -t spring-api:v1 .

# Run
docker run -d \
  --name spring-api \
  -p 8080:8080 \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://host:5432/springdb \
  spring-api:v1

# Con Docker Compose
docker compose --profile production up -d
```

**Desarrollo con Docker:**
```bash
docker compose --profile development up -d
docker compose logs -f api-dev
```

**Probar API:**
```bash
curl http://localhost:8080
curl http://localhost:8080/health
curl http://localhost:8080/api/users

# Crear usuario
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan","email":"juan@example.com"}'
```

---

## Optimizaciones

### 1. Usar Spring Boot Layered JARs

```dockerfile
FROM eclipse-temurin:17-jre-alpine AS builder
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

ENTRYPOINT ["java", "org.springframework.boot.loader.JarLauncher"]
```

### 2. Usar Maven Wrapper en Docker

```dockerfile
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
RUN ./mvnw dependency:go-offline
COPY src ./src
RUN ./mvnw clean package -DskipTests
```

### 3. Configuración de JVM

```dockerfile
ENTRYPOINT ["java", \
    "-XX:+UseContainerSupport", \
    "-XX:MaxRAMPercentage=75.0", \
    "-jar", "app.jar"]
```

---

## Testing

**src/test/java/com/ejemplo/apispring/UserControllerTest.java:**
```java
package com.ejemplo.apispring;

import com.ejemplo.apispring.controller.UserController;
import com.ejemplo.apispring.model.User;
import com.ejemplo.apispring.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
public class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    public void getAllUsers_ReturnsListOfUsers() throws Exception {
        User user1 = new User();
        user1.setId(1L);
        user1.setName("Juan");
        user1.setEmail("juan@example.com");

        when(userService.getAllUsers()).thenReturn(Arrays.asList(user1));

        mockMvc.perform(get("/api/users"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Juan"));
    }

    @Test
    public void getUserById_ReturnsUser() throws Exception {
        User user = new User();
        user.setId(1L);
        user.setName("Juan");

        when(userService.getUserById(1L)).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Juan"));
    }
}
```

**Ejecutar tests:**
```bash
./mvnw test

# Con Docker
docker build -f Dockerfile.test -t spring-api-test .
docker run --rm spring-api-test
```

---

## Ejercicios Prácticos

### Ejercicio 1: CRUD Completo
Implementa entidades relacionadas:
- User (ya existe)
- Post (1 user -> muchos posts)
- Comment (1 post -> muchos comments)

### Ejercicio 2: Paginación y Búsqueda
```java
@GetMapping
public ResponseEntity<Page<User>> getAllUsers(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "10") int size,
    @RequestParam(required = false) String search
) {
    // Implementar
}
```

### Ejercicio 3: Spring Security + JWT
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt</artifactId>
    <version>0.9.1</version>
</dependency>
```

### Ejercicio 4: Documentación con OpenAPI/Swagger
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

Acceder en: `http://localhost:8080/swagger-ui.html`

---

## Troubleshooting

### Maven build falla
```bash
# Limpiar y rebuild
./mvnw clean install

# Skip tests
./mvnw clean package -DskipTests
```

### Base de datos no conecta
```bash
# Verificar logs
docker compose logs db

# Probar conexión manual
docker compose exec db psql -U usuario -d springdb
```

### Out of Memory en Docker
```dockerfile
# Agregar límites de memoria
ENTRYPOINT ["java", "-Xmx512m", "-Xms256m", "-jar", "app.jar"]
```

---

## Resumen de Comandos

```bash
# Maven local
./mvnw spring-boot:run
./mvnw clean package
./mvnw test

# Docker
docker build -t spring-api:v1 .
docker run -d --name spring-api -p 8080:8080 spring-api:v1

# Docker Compose
docker compose --profile production up -d
docker compose --profile development up -d
docker compose logs -f
docker compose down

# Acceder a contenedor
docker exec -it spring-api sh
```

---

## Checklist del Proyecto

- [ ] Crear proyecto Spring Boot
- [ ] Configurar pom.xml
- [ ] Configurar application.properties
- [ ] Crear modelos JPA
- [ ] Crear repositorios
- [ ] Crear servicios
- [ ] Crear controladores REST
- [ ] Crear Dockerfile multi-stage
- [ ] Crear .dockerignore
- [ ] Construir imagen
- [ ] Crear docker-compose.yml
- [ ] Integrar PostgreSQL
- [ ] Probar endpoints CRUD
- [ ] Escribir tests
- [ ] Agregar documentación Swagger

---

## Siguiente Paso

Continúa con:
**[Proyecto 8: Full Stack Completo](./08-fullstack-completo.md)**
