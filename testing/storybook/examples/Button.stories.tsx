import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
    title: 'Atomic/Button',
    component: Button,
    argTypes: {
        backgroundColor: { control: 'color' },
    },
};

export default meta;
type Story = StoryObj<typeof Button>;

// 1. Snapshot Test Básico
export const Primary: Story = {
    args: {
        primary: true,
        label: 'Button',
    },
};

// 2. Interaction Test: Hover & Click
export const ClickInteraction: Story = {
    args: {
        label: 'Click Me',
    },
    play: async ({ canvasElement }: { canvasElement: HTMLElement }) => {
        const canvas = within(canvasElement);
        const button = canvas.getByRole('button');

        // Verificación inicial
        await expect(button).toBeInTheDocument();

        // Simular Clic
        await userEvent.click(button);

        // Si el botón cambia de estado al hacer clic, lo verificamos
        // await expect(canvas.getByText('Clicked!')).toBeInTheDocument();
    },
};

// 3. Test de Accesibilidad (Simulado)
export const LargeAndClear: Story = {
    args: {
        size: 'large',
        label: 'Accessible Button',
        'aria-label': 'Boton grande accesible',
    },
};
