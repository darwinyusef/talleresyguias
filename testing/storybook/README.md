# 🎨 Storybook Testing: Guía Completa de Pruebas de UI

Storybook no es solo una herramienta para documentar componentes; es una poderosa plataforma de **Testing de Interfaz de Usuario**. Esta sección del taller cubre cómo transformar tu biblioteca de componentes en una suite de pruebas automatizada.

## 🚀 ¿Qué es Storybook Testing?

Tradicionalmente, las pruebas de UI se hacían con herramientas de E2E pesadas. Storybook permite probar componentes en **aislamiento**, lo que las hace más rápidas y fáciles de mantener.

### Tipos de Pruebas cubiertas en este módulo:

1.  **[Visual Regression Testing](./01-visual-testing.md)**: Detecta cambios de píxeles inesperados.
2.  **[Interaction Testing (Play Function)](./02-interaction-testing.md)**: Simula clics y entradas de usuario directamente en el componente.
3.  **[Accessibility Testing (a11y)](./03-accessibility.md)**: Asegura que tus componentes sean usables por todos.
4.  **[Snapshot Testing](./04-snapshots.md)**: Pruebas estructurales automáticas a partir de tus historias.

---

## 🛠️ Configuración Inicial

Para habilitar las funciones de testing en tu proyecto de Storybook:

```bash
# Instalar el test-runner de Storybook
npm install @storybook/test-runner --save-dev

# Instalar addons de interacción y accesibilidad
npm install @storybook/addon-interactions @storybook/addon-a11y @storybook/testing-library @storybook/jest --save-dev
```

## 🏁 Flujo de Trabajo Recomendado

1.  **Define tu Historia**: Crea un archivo `.stories.tsx`.
2.  **Añade Interacciones**: Usa la función `play` para simular estados.
3.  **Corre el Runner**: Ejecuta `npm run test-storybook` para validar todas tus historias en modo headless (Playwright).

---

## 📂 Ejemplos Disponibles
- [Componente de Botón con Tests](./examples/Button.stories.tsx)
- [Formulario de Login con Interacciones](./examples/LoginForm.stories.tsx)
