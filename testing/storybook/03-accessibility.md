# ♿ Accessibility Testing (a11y)

El 20% de los usuarios de internet tienen alguna discapacidad. Probar la accesibilidad asegura que todos puedan usar tu producto y te ayuda a cumplir normas legales (WCAG).

## 🛠️ Addon a11y

Instalando `@storybook/addon-a11y`, obtendrás un panel automático que escanea tus componentes en busca de:
- Contrastes de color insuficientes.
- Elementos sin etiquetas ARIA.
- Errores estructurales (ej. IDs duplicados).

## Ejemplo: Componente con Errores

Si creas una historia para un botón que solo tiene un icono y no tiene `aria-label`, el addon marcará un error crítico.

```tsx
// Este componente fallará el test de a11y
export const AccessibleButton = () => (
  <button>
    <img src="trash.png" />
  </button>
);

// Este componente pasará
export const BetterButton = () => (
  <button aria-label="Eliminar elemento">
    <img src="trash.png" alt="" />
  </button>
);
```

## 🤖 Automatización en Terminal

Puedes integrar las pruebas de accesibilidad en tu runner:

```javascript
// .storybook/test-runner.js
const { injectAxe, checkA11y } = require('axe-playwright');

module.exports = {
  async preRender(page) {
    await injectAxe(page);
  },
  async postRender(page) {
    await checkA11y(page, '#storybook-root', {
      detailedReport: true,
      detailedReportOptions: { html: true },
    });
  },
};
```
Cada vez que corras `test-storybook`, se ejecutará un escaneo de **Axe** sobre cada componente.
