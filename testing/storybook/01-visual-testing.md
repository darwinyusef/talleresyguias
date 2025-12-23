# 👁️ Visual Regression Testing

El Visual Testing (o Snapshot testing de imagen) captura una "foto" de tu componente y la compara con una línea base (baseline) anterior. Si un solo píxel cambia, la prueba falla.

## 🛠️ Herramientas Populares
- **Chromatic**: La herramienta oficial de los creadores de Storybook (hospedada).
- **Storyshots + Jest-Image-Snapshot**: Solución self-hosted.
- **Playwright/Cypress**: Integrados con Storybook.

## 💡 ¿Por qué Visual Testing?
Imagina que cambias un color global en tu CSS. Las pruebas unitarias de lógica pasarán, pero tus componentes podrían verse mal (ej. texto azul sobre fondo azul). El Visual Testing atrapa esto instantáneamente.

## Ejemplo de Configuración con Playwright logic

```javascript
// En tu test runner config
const { injectAxe, checkA11y } = require('axe-playwright');

module.exports = {
  async postRender(page, context) {
    // Si queremos capturar un screenshot de cada historia automáticamente
    await page.screenshot({ path: `screenshots/${context.id}.png` });
  },
};
```

## Ventajas
- **Cobertura total de UI** sin escribir tests manuales por componente.
- **Detección de "Side Effects"** en CSS global.
