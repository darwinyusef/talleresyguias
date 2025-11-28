# Curso de Testing en Python: De Cero a Experto

Bienvenido al curso completo de testing en Python. Este curso está diseñado para personas sin conocimientos previos de testing y te llevará desde los conceptos básicos hasta realizar pruebas end-to-end completas.

## ¿Qué aprenderás?

- Fundamentos de testing y por qué es importante
- Test unitarios con pytest
- Testing de código orientado a objetos
- Testing de servicios y APIs
- Test de integración con mocks
- Test End-to-End con Cypress

## Requisitos Previos

- Conocimientos básicos de Python
- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)
- Node.js (para la sección de Cypress)

## Estructura del Curso

### [Módulo 1: Introducción a Testing y Pytest](modulos/01-introduccion-testing-pytest.md)
- ¿Qué es el testing?
- Tipos de testing
- Instalación y configuración de pytest
- Tu primer test
- Assertions básicas
- Ejecutar tests

### [Módulo 2: Test Unitarios Básicos](modulos/02-test-unitarios-basicos.md)
- Funciones simples y puras
- Testing de operaciones matemáticas
- Testing de strings y listas
- Parametrización de tests
- Fixtures básicas
- Tests de excepciones

### [Módulo 3: Test Unitarios con POO](modulos/03-test-unitarios-poo.md)
- Testing de clases y objetos
- Testing de métodos
- Testing de propiedades
- Testing de herencia
- Testing de métodos estáticos y de clase
- Setup y teardown en clases

### [Módulo 4: Test Unitarios a Servicios](modulos/04-test-unitarios-servicios.md)
- Testing de servicios HTTP
- Mocking de requests
- Testing de APIs REST
- Testing de respuestas JSON
- Manejo de errores en servicios
- Testing asíncrono

### [Módulo 5: Test de Integración con Mocks (CRUD)](modulos/05-test-integracion-mocks.md)
- Introducción a los mocks
- Mock de bases de datos
- Testing CRUD: Create
- Testing CRUD: Read
- Testing CRUD: Update
- Testing CRUD: Delete
- Integración completa del CRUD

### [Módulo 6: Test E2E con Cypress](modulos/06-test-e2e-cypress.md)
- Introducción a Cypress
- Instalación y configuración
- Estructura de tests en Cypress
- Selectores y comandos básicos
- Testing de formularios
- Testing de flujos completos
- Integración frontend-backend

## Instalación Rápida

```bash
# Clonar o descargar el curso
cd curso-testing-python

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias para Python
pip install pytest pytest-cov pytest-mock requests

# Para el módulo de Cypress (ejecutar en la carpeta de ejemplos)
cd ejemplos/06-e2e-cypress
npm install
```

## Cómo Usar Este Curso

1. Lee cada módulo en orden secuencial
2. Practica con los ejemplos incluidos en la carpeta `ejemplos/`
3. Intenta modificar los tests para entender mejor
4. Completa los ejercicios propuestos al final de cada módulo
5. Crea tus propios tests para proyectos personales

## Estructura de Carpetas

```
curso-testing-python/
├── README.md
├── modulos/
│   ├── 01-introduccion-testing-pytest.md
│   ├── 02-test-unitarios-basicos.md
│   ├── 03-test-unitarios-poo.md
│   ├── 04-test-unitarios-servicios.md
│   ├── 05-test-integracion-mocks.md
│   └── 06-test-e2e-cypress.md
└── ejemplos/
    ├── 01-basicos/
    ├── 02-poo/
    ├── 03-servicios/
    ├── 04-integracion/
    ├── 05-mocks-crud/
    └── 06-e2e-cypress/
```

## Recursos Adicionales

- [Documentación oficial de pytest](https://docs.pytest.org/)
- [Documentación oficial de Cypress](https://docs.cypress.io/)
- [Python Testing with pytest (libro)](https://pragprog.com/titles/bopytest/)

## Contribuciones

Este curso es un material educativo. Si encuentras errores o tienes sugerencias, no dudes en mejorar el contenido.

## Licencia

Material educativo de uso libre.

---

**¡Comienza ahora con el [Módulo 1: Introducción a Testing y Pytest](modulos/01-introduccion-testing-pytest.md)!**
