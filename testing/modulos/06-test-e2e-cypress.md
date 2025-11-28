# Módulo 6: Test End-to-End con Cypress

## Introducción

En este módulo aprenderás a crear tests End-to-End (E2E) usando Cypress. Los tests E2E verifican que todo el sistema funcione correctamente desde la perspectiva del usuario, integrando frontend y backend.

## ¿Qué es Cypress?

Cypress es un framework de testing moderno para aplicaciones web que te permite:
- Testear flujos completos de usuario
- Verificar interacciones de UI
- Testear APIs
- Realizar testing visual
- Debuggear fácilmente

## Diferencias con Testing de Python

| Aspecto | Pytest (Python) | Cypress (JavaScript) |
|---------|----------------|---------------------|
| Lenguaje | Python | JavaScript |
| Enfoque | Backend, unitarios | Frontend, E2E |
| Scope | Funciones, clases | Usuario final |
| Velocidad | Muy rápido | Más lento |
| Browser | No requiere | Requiere navegador |

## Instalación de Cypress

### Requisitos Previos

```bash
# Verificar Node.js instalado
node --version  # Debe ser v12 o superior
npm --version
```

### Instalación

**Crear proyecto nuevo:**
```bash
# Navegar a la carpeta de ejemplos
cd ejemplos/06-e2e-cypress

# Inicializar proyecto Node.js
npm init -y

# Instalar Cypress
npm install cypress --save-dev

# Abrir Cypress por primera vez
npx cypress open
```

Esto creará la siguiente estructura:

```
ejemplos/06-e2e-cypress/
├── cypress/
│   ├── e2e/              # Tests E2E
│   ├── fixtures/         # Datos de prueba
│   ├── support/          # Comandos personalizados
│   └── downloads/        # Archivos descargados
├── cypress.config.js     # Configuración
├── package.json
└── node_modules/
```

## Configuración Básica

**Archivo: cypress.config.js**
```javascript
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      // Configuración de eventos
    },
  },
})
```

## Estructura de un Test en Cypress

### Sintaxis Básica

**Archivo: cypress/e2e/01-primer-test.cy.js**
```javascript
describe('Mi Primer Test en Cypress', () => {

  it('Debería visitar la página principal', () => {
    // Visitar URL
    cy.visit('/')

    // Verificar título
    cy.title().should('include', 'Mi App')
  })

  it('Debería encontrar un elemento', () => {
    cy.visit('/')

    // Buscar por texto
    cy.contains('Bienvenido')

    // Buscar por selector
    cy.get('#main-title').should('be.visible')
  })
})
```

## Selectores en Cypress

### Tipos de Selectores

**Archivo: cypress/e2e/02-selectores.cy.js**
```javascript
describe('Selectores en Cypress', () => {

  beforeEach(() => {
    cy.visit('/')
  })

  it('Selectores CSS básicos', () => {
    // Por ID
    cy.get('#username')

    // Por clase
    cy.get('.btn-primary')

    // Por atributo
    cy.get('[data-testid="submit-button"]')

    // Por tipo
    cy.get('input[type="email"]')
  })

  it('Selectores por contenido', () => {
    // Texto exacto
    cy.contains('Iniciar Sesión')

    // Texto parcial
    cy.contains('Iniciar')

    // Dentro de un elemento
    cy.get('form').contains('Enviar')
  })

  it('Selectores avanzados', () => {
    // Primer elemento
    cy.get('li').first()

    // Último elemento
    cy.get('li').last()

    // Por índice
    cy.get('li').eq(2)

    // Filtrar
    cy.get('button').filter('.active')
  })
})
```

## Testing de Formularios

### Ejemplo: Formulario de Registro

**Archivo: cypress/e2e/03-formulario-registro.cy.js**
```javascript
describe('Formulario de Registro', () => {

  beforeEach(() => {
    cy.visit('/register')
  })

  it('Debería registrar un usuario nuevo', () => {
    // Llenar campos
    cy.get('[data-testid="input-nombre"]')
      .type('Juan Pérez')

    cy.get('[data-testid="input-email"]')
      .type('juan@email.com')

    cy.get('[data-testid="input-password"]')
      .type('Password123!')

    cy.get('[data-testid="input-password-confirm"]')
      .type('Password123!')

    // Seleccionar checkbox
    cy.get('[data-testid="checkbox-terms"]')
      .check()

    // Enviar formulario
    cy.get('[data-testid="btn-submit"]')
      .click()

    // Verificar redirección
    cy.url().should('include', '/dashboard')

    // Verificar mensaje de éxito
    cy.contains('Registro exitoso')
  })

  it('Debería mostrar errores de validación', () => {
    // Intentar enviar sin llenar
    cy.get('[data-testid="btn-submit"]').click()

    // Verificar mensajes de error
    cy.contains('El nombre es requerido')
    cy.contains('El email es requerido')
  })

  it('Debería validar formato de email', () => {
    cy.get('[data-testid="input-email"]')
      .type('email-invalido')
      .blur()

    cy.contains('Email inválido')
  })

  it('Debería validar que las contraseñas coincidan', () => {
    cy.get('[data-testid="input-password"]')
      .type('Password123!')

    cy.get('[data-testid="input-password-confirm"]')
      .type('OtraPassword')
      .blur()

    cy.contains('Las contraseñas no coinciden')
  })
})
```

## Testing de Autenticación

**Archivo: cypress/e2e/04-autenticacion.cy.js**
```javascript
describe('Sistema de Autenticación', () => {

  it('Debería iniciar sesión correctamente', () => {
    cy.visit('/login')

    // Llenar formulario
    cy.get('[data-testid="input-email"]')
      .type('usuario@email.com')

    cy.get('[data-testid="input-password"]')
      .type('password123')

    // Enviar
    cy.get('[data-testid="btn-login"]').click()

    // Verificar redirección
    cy.url().should('include', '/dashboard')

    // Verificar que aparece nombre de usuario
    cy.get('[data-testid="user-name"]')
      .should('contain', 'Usuario')
  })

  it('Debería mostrar error con credenciales incorrectas', () => {
    cy.visit('/login')

    cy.get('[data-testid="input-email"]')
      .type('usuario@email.com')

    cy.get('[data-testid="input-password"]')
      .type('password-incorrecta')

    cy.get('[data-testid="btn-login"]').click()

    // Verificar mensaje de error
    cy.contains('Credenciales incorrectas')

    // Verificar que permanece en login
    cy.url().should('include', '/login')
  })

  it('Debería cerrar sesión', () => {
    // Primero iniciar sesión
    cy.visit('/login')
    cy.get('[data-testid="input-email"]').type('usuario@email.com')
    cy.get('[data-testid="input-password"]').type('password123')
    cy.get('[data-testid="btn-login"]').click()

    // Cerrar sesión
    cy.get('[data-testid="btn-logout"]').click()

    // Verificar redirección a login
    cy.url().should('include', '/login')
  })
})
```

## Testing de CRUD con Cypress

**Archivo: cypress/e2e/05-crud-usuarios.cy.js**
```javascript
describe('CRUD de Usuarios', () => {

  beforeEach(() => {
    // Login antes de cada test
    cy.visit('/login')
    cy.get('[data-testid="input-email"]').type('admin@email.com')
    cy.get('[data-testid="input-password"]').type('admin123')
    cy.get('[data-testid="btn-login"]').click()
    cy.url().should('include', '/dashboard')
  })

  describe('CREATE - Crear Usuario', () => {
    it('Debería crear un nuevo usuario', () => {
      // Ir a página de usuarios
      cy.visit('/usuarios')

      // Click en botón nuevo
      cy.get('[data-testid="btn-nuevo-usuario"]').click()

      // Llenar formulario
      cy.get('[data-testid="input-nombre"]').type('Nuevo Usuario')
      cy.get('[data-testid="input-email"]').type('nuevo@email.com')
      cy.get('[data-testid="input-edad"]').type('25')

      // Guardar
      cy.get('[data-testid="btn-guardar"]').click()

      // Verificar que aparece en la lista
      cy.get('[data-testid="tabla-usuarios"]')
        .should('contain', 'Nuevo Usuario')
        .and('contain', 'nuevo@email.com')
    })
  })

  describe('READ - Leer Usuarios', () => {
    it('Debería mostrar lista de usuarios', () => {
      cy.visit('/usuarios')

      // Verificar que la tabla existe
      cy.get('[data-testid="tabla-usuarios"]').should('be.visible')

      // Verificar que hay al menos un usuario
      cy.get('[data-testid="fila-usuario"]').should('have.length.at.least', 1)
    })

    it('Debería buscar usuarios', () => {
      cy.visit('/usuarios')

      // Escribir en buscador
      cy.get('[data-testid="input-buscar"]').type('Juan')

      // Verificar resultados filtrados
      cy.get('[data-testid="fila-usuario"]').each(($fila) => {
        cy.wrap($fila).should('contain', 'Juan')
      })
    })

    it('Debería ver detalle de usuario', () => {
      cy.visit('/usuarios')

      // Click en primer usuario
      cy.get('[data-testid="fila-usuario"]').first().click()

      // Verificar modal o página de detalle
      cy.get('[data-testid="modal-detalle"]').should('be.visible')
      cy.get('[data-testid="detalle-nombre"]').should('not.be.empty')
    })
  })

  describe('UPDATE - Actualizar Usuario', () => {
    it('Debería editar un usuario', () => {
      cy.visit('/usuarios')

      // Click en botón editar del primer usuario
      cy.get('[data-testid="btn-editar"]').first().click()

      // Cambiar nombre
      cy.get('[data-testid="input-nombre"]')
        .clear()
        .type('Nombre Actualizado')

      // Guardar
      cy.get('[data-testid="btn-guardar"]').click()

      // Verificar cambio
      cy.get('[data-testid="tabla-usuarios"]')
        .should('contain', 'Nombre Actualizado')
    })

    it('Debería validar datos al editar', () => {
      cy.visit('/usuarios')

      cy.get('[data-testid="btn-editar"]').first().click()

      // Intentar guardar con email inválido
      cy.get('[data-testid="input-email"]')
        .clear()
        .type('email-invalido')

      cy.get('[data-testid="btn-guardar"]').click()

      // Verificar error
      cy.contains('Email inválido')
    })
  })

  describe('DELETE - Eliminar Usuario', () => {
    it('Debería eliminar un usuario', () => {
      cy.visit('/usuarios')

      // Obtener nombre del primer usuario
      cy.get('[data-testid="fila-usuario"]')
        .first()
        .find('[data-testid="nombre-usuario"]')
        .invoke('text')
        .then((nombre) => {
          // Click en eliminar
          cy.get('[data-testid="btn-eliminar"]').first().click()

          // Confirmar en modal
          cy.get('[data-testid="btn-confirmar-eliminar"]').click()

          // Verificar que ya no existe
          cy.get('[data-testid="tabla-usuarios"]')
            .should('not.contain', nombre)
        })
    })

    it('Debería cancelar eliminación', () => {
      cy.visit('/usuarios')

      // Contar usuarios iniciales
      cy.get('[data-testid="fila-usuario"]')
        .its('length')
        .then((countInicial) => {
          // Intentar eliminar
          cy.get('[data-testid="btn-eliminar"]').first().click()

          // Cancelar
          cy.get('[data-testid="btn-cancelar"]').click()

          // Verificar que sigue ahí
          cy.get('[data-testid="fila-usuario"]')
            .should('have.length', countInicial)
        })
    })
  })
})
```

## Comandos Personalizados

Los comandos personalizados te permiten reutilizar código común.

**Archivo: cypress/support/commands.js**
```javascript
// Comando para login
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('[data-testid="input-email"]').type(email)
  cy.get('[data-testid="input-password"]').type(password)
  cy.get('[data-testid="btn-login"]').click()
  cy.url().should('include', '/dashboard')
})

// Comando para crear usuario
Cypress.Commands.add('crearUsuario', (nombre, email, edad) => {
  cy.get('[data-testid="btn-nuevo-usuario"]').click()
  cy.get('[data-testid="input-nombre"]').type(nombre)
  cy.get('[data-testid="input-email"]').type(email)
  cy.get('[data-testid="input-edad"]').type(edad)
  cy.get('[data-testid="btn-guardar"]').click()
})

// Comando para logout
Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="btn-logout"]').click()
})

// Comando para esperar API
Cypress.Commands.add('esperarAPI', (alias) => {
  cy.wait(`@${alias}`)
})
```

### Uso de Comandos Personalizados

**Archivo: cypress/e2e/06-usando-comandos.cy.js**
```javascript
describe('Usando Comandos Personalizados', () => {

  it('Debería usar comando de login', () => {
    cy.login('admin@email.com', 'admin123')
    cy.contains('Dashboard')
  })

  it('Debería crear usuario con comando', () => {
    cy.login('admin@email.com', 'admin123')
    cy.visit('/usuarios')

    cy.crearUsuario('Test Usuario', 'test@email.com', '30')

    cy.get('[data-testid="tabla-usuarios"]')
      .should('contain', 'Test Usuario')
  })

  it('Flujo completo con comandos', () => {
    // Login
    cy.login('admin@email.com', 'admin123')

    // Crear usuario
    cy.visit('/usuarios')
    cy.crearUsuario('Juan', 'juan@email.com', '25')

    // Logout
    cy.logout()
    cy.url().should('include', '/login')
  })
})
```

## Testing de APIs con Cypress

Cypress también puede testear APIs directamente.

**Archivo: cypress/e2e/07-testing-api.cy.js**
```javascript
describe('Testing de API', () => {

  const API_URL = 'http://localhost:8000/api'

  it('Debería obtener lista de usuarios', () => {
    cy.request(`${API_URL}/usuarios`)
      .then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.be.an('array')
        expect(response.body.length).to.be.greaterThan(0)
      })
  })

  it('Debería crear un usuario vía API', () => {
    cy.request({
      method: 'POST',
      url: `${API_URL}/usuarios`,
      body: {
        nombre: 'Usuario API',
        email: 'api@email.com',
        edad: 28
      }
    }).then((response) => {
      expect(response.status).to.eq(201)
      expect(response.body).to.have.property('id')
      expect(response.body.nombre).to.eq('Usuario API')
    })
  })

  it('Debería actualizar un usuario', () => {
    // Primero crear
    cy.request('POST', `${API_URL}/usuarios`, {
      nombre: 'Usuario Temp',
      email: 'temp@email.com',
      edad: 25
    }).then((createResponse) => {
      const userId = createResponse.body.id

      // Actualizar
      cy.request('PUT', `${API_URL}/usuarios/${userId}`, {
        nombre: 'Usuario Actualizado'
      }).then((updateResponse) => {
        expect(updateResponse.status).to.eq(200)
        expect(updateResponse.body.nombre).to.eq('Usuario Actualizado')
      })
    })
  })

  it('Debería eliminar un usuario', () => {
    // Crear usuario
    cy.request('POST', `${API_URL}/usuarios`, {
      nombre: 'Usuario Temporal',
      email: 'temporal@email.com',
      edad: 25
    }).then((response) => {
      const userId = response.body.id

      // Eliminar
      cy.request('DELETE', `${API_URL}/usuarios/${userId}`)
        .its('status')
        .should('eq', 204)
    })
  })
})
```

## Interceptando Requests

**Archivo: cypress/e2e/08-interceptar-requests.cy.js**
```javascript
describe('Interceptar Requests', () => {

  it('Debería interceptar llamada GET', () => {
    // Interceptar request
    cy.intercept('GET', '/api/usuarios').as('obtenerUsuarios')

    cy.visit('/usuarios')

    // Esperar request
    cy.wait('@obtenerUsuarios').then((interception) => {
      expect(interception.response.statusCode).to.eq(200)
      expect(interception.response.body).to.be.an('array')
    })
  })

  it('Debería mockear respuesta de API', () => {
    // Mockear respuesta
    cy.intercept('GET', '/api/usuarios', {
      statusCode: 200,
      body: [
        { id: 1, nombre: 'Usuario Mock', email: 'mock@email.com', edad: 25 }
      ]
    }).as('usuariosMockeados')

    cy.visit('/usuarios')

    cy.wait('@usuariosMockeados')

    // Verificar que muestra datos mockeados
    cy.get('[data-testid="tabla-usuarios"]')
      .should('contain', 'Usuario Mock')
  })

  it('Debería simular error de API', () => {
    // Simular error
    cy.intercept('GET', '/api/usuarios', {
      statusCode: 500,
      body: { error: 'Error del servidor' }
    })

    cy.visit('/usuarios')

    // Verificar mensaje de error
    cy.contains('Error al cargar usuarios')
  })
})
```

## Fixtures (Datos de Prueba)

**Archivo: cypress/fixtures/usuarios.json**
```json
{
  "usuarioValido": {
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "edad": 25
  },
  "listaUsuarios": [
    {
      "id": 1,
      "nombre": "Ana García",
      "email": "ana@email.com",
      "edad": 30
    },
    {
      "id": 2,
      "nombre": "Pedro López",
      "email": "pedro@email.com",
      "edad": 35
    }
  ]
}
```

**Usando fixtures:**

**Archivo: cypress/e2e/09-usando-fixtures.cy.js**
```javascript
describe('Usando Fixtures', () => {

  it('Debería usar datos de fixture', () => {
    cy.fixture('usuarios').then((data) => {
      const usuario = data.usuarioValido

      cy.visit('/register')
      cy.get('[data-testid="input-nombre"]').type(usuario.nombre)
      cy.get('[data-testid="input-email"]').type(usuario.email)
      cy.get('[data-testid="input-edad"]').type(usuario.edad)
    })
  })

  it('Debería mockear con datos de fixture', () => {
    cy.intercept('GET', '/api/usuarios', {
      fixture: 'usuarios.json'
    }).as('usuarios')

    cy.visit('/usuarios')
    cy.wait('@usuarios')

    cy.get('[data-testid="fila-usuario"]')
      .should('have.length', 2)
  })
})
```

## Flujo E2E Completo

**Archivo: cypress/e2e/10-flujo-completo.cy.js**
```javascript
describe('Flujo E2E Completo: Gestión de Usuarios', () => {

  const timestamp = Date.now()
  const nuevoUsuario = {
    nombre: `Usuario Test ${timestamp}`,
    email: `test${timestamp}@email.com`,
    edad: '25'
  }

  it('Flujo completo: Registro → Login → CRUD → Logout', () => {
    // 1. REGISTRO
    cy.visit('/register')
    cy.get('[data-testid="input-nombre"]').type(nuevoUsuario.nombre)
    cy.get('[data-testid="input-email"]').type(nuevoUsuario.email)
    cy.get('[data-testid="input-password"]').type('Password123!')
    cy.get('[data-testid="input-password-confirm"]').type('Password123!')
    cy.get('[data-testid="checkbox-terms"]').check()
    cy.get('[data-testid="btn-submit"]').click()

    cy.url().should('include', '/dashboard')
    cy.contains('Bienvenido')

    // 2. NAVEGAR A USUARIOS
    cy.get('[data-testid="menu-usuarios"]').click()
    cy.url().should('include', '/usuarios')

    // 3. CREAR NUEVO USUARIO
    cy.get('[data-testid="btn-nuevo-usuario"]').click()
    cy.get('[data-testid="input-nombre"]').type('Nuevo Contacto')
    cy.get('[data-testid="input-email"]').type(`contacto${timestamp}@email.com`)
    cy.get('[data-testid="input-edad"]').type('30')
    cy.get('[data-testid="btn-guardar"]').click()

    // Verificar creación
    cy.contains('Usuario creado exitosamente')
    cy.get('[data-testid="tabla-usuarios"]').should('contain', 'Nuevo Contacto')

    // 4. BUSCAR USUARIO
    cy.get('[data-testid="input-buscar"]').type('Nuevo Contacto')
    cy.get('[data-testid="fila-usuario"]').should('have.length', 1)

    // 5. EDITAR USUARIO
    cy.get('[data-testid="btn-editar"]').click()
    cy.get('[data-testid="input-nombre"]').clear().type('Contacto Editado')
    cy.get('[data-testid="btn-guardar"]').click()

    cy.contains('Usuario actualizado')
    cy.get('[data-testid="tabla-usuarios"]').should('contain', 'Contacto Editado')

    // 6. VER PERFIL
    cy.get('[data-testid="menu-perfil"]').click()
    cy.get('[data-testid="perfil-nombre"]').should('contain', nuevoUsuario.nombre)

    // 7. ELIMINAR USUARIO
    cy.get('[data-testid="menu-usuarios"]').click()
    cy.get('[data-testid="input-buscar"]').clear().type('Contacto Editado')
    cy.get('[data-testid="btn-eliminar"]').click()
    cy.get('[data-testid="btn-confirmar-eliminar"]').click()

    cy.contains('Usuario eliminado')

    // 8. LOGOUT
    cy.get('[data-testid="btn-logout"]').click()
    cy.url().should('include', '/login')
  })
})
```

## Mejores Prácticas

### 1. Usar data-testid

```html
<!-- Bueno -->
<button data-testid="btn-submit">Enviar</button>

<!-- Evitar -->
<button class="btn btn-primary submit-btn">Enviar</button>
```

### 2. Esperas Inteligentes

```javascript
// Bueno - Cypress espera automáticamente
cy.get('[data-testid="elemento"]').should('be.visible')

// Evitar - Esperas fijas
cy.wait(1000)
```

### 3. Organización de Tests

```javascript
describe('Módulo de Usuarios', () => {
  beforeEach(() => {
    cy.login('admin@email.com', 'admin123')
  })

  describe('Crear Usuario', () => {
    // Tests de creación
  })

  describe('Editar Usuario', () => {
    // Tests de edición
  })
})
```

## Ejecutar Tests

```bash
# Modo interactivo
npx cypress open

# Modo headless (CI/CD)
npx cypress run

# Ejecutar archivo específico
npx cypress run --spec "cypress/e2e/05-crud-usuarios.cy.js"

# Con navegador específico
npx cypress run --browser chrome

# Generar video
npx cypress run --video
```

## Ejemplo de package.json

**Archivo: package.json**
```json
{
  "name": "cypress-e2e-tests",
  "version": "1.0.0",
  "scripts": {
    "cy:open": "cypress open",
    "cy:run": "cypress run",
    "cy:run:chrome": "cypress run --browser chrome",
    "test:e2e": "cypress run --headless"
  },
  "devDependencies": {
    "cypress": "^12.0.0"
  }
}
```

## Ejercicios Prácticos

### Ejercicio 1: E-commerce Completo

```markdown
Crea tests E2E para un e-commerce:

- Registro de usuario
- Login
- Buscar productos
- Agregar al carrito
- Modificar cantidad
- Proceso de checkout
- Ver historial de pedidos
- Logout
```

### Ejercicio 2: Dashboard Administrativo

```markdown
Tests para dashboard admin:

- Login como admin
- Ver estadísticas
- Gestión de usuarios (CRUD)
- Gestión de productos (CRUD)
- Ver reportes
- Exportar datos
```

### Ejercicio 3: Aplicación Social

```markdown
Tests para red social:

- Registro
- Crear publicación
- Like/Unlike
- Comentar
- Seguir/Dejar de seguir usuarios
- Ver feed
- Editar perfil
```

## Resumen

En este módulo aprendiste:

- Qué es Cypress y cómo instalarlo
- Estructura de tests E2E
- Selectores y comandos básicos
- Testing de formularios
- Testing de autenticación
- Testing de CRUD completo
- Comandos personalizados
- Testing de APIs
- Interceptar y mockear requests
- Fixtures para datos de prueba
- Flujos E2E completos
- Mejores prácticas

## Conclusión del Curso

¡Felicidades! Has completado el curso de testing desde cero. Ahora sabes:

- Fundamentos de testing
- Test unitarios con pytest
- Testing de POO
- Testing de servicios
- Test de integración con mocks
- Test E2E con Cypress

## Próximos Pasos

- Practica con proyectos reales
- Explora testing de performance
- Aprende sobre CI/CD
- Investiga testing visual
- Profundiza en TDD (Test-Driven Development)

---

**[⬅️ Módulo anterior](05-test-integracion-mocks.md) | [Volver al índice](../README.md)**
