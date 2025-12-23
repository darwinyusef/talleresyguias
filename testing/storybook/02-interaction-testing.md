# 🖱️ Interaction Testing (The Play Function)

Storybook te permite escribir pruebas que se ejecutan **dentro del navegador**, simulando interacciones de usuario. Esto sustituye en gran medida a muchos tests de React Testing Library.

## 🎭 La Función `play`

La función `play` se ejecuta después de que el componente se renderiza en el Storybook. Usa una versión de `Jest` y `Testing Library` adaptada para el navegador.

## Ejemplo: Test de Formulario de Login

```tsx
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { LoginForm } from './LoginForm';

export default {
  title: 'Components/LoginForm',
  component: LoginForm,
};

export const FilledForm = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Simular escritura en email
    await userEvent.type(canvas.getByTestId('email'), 'test@example.com', {
      delay: 100,
    });

    // Simular escritura en password
    await userEvent.type(canvas.getByTestId('password'), 'password123', {
      delay: 100,
    });

    // Clic en el botón de submit
    await userEvent.click(canvas.getByRole('button'));

    // Validar estado esperado
    await expect(canvas.getByText('Enviando...')).toBeInTheDocument();
  },
};
```

## 🚀 Ejecución Automatizada
Puedes correr estos tests en tu CI/CD usando el **Storybook Test Runner**:

```bash
test-storybook --url http://localhost:6006
```
Esto abrirá cada historia, ejecutará su función `play` y reportará si alguna aserción de `expect` falló.
