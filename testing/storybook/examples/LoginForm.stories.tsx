import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { LoginForm } from './LoginForm';

const meta: Meta<typeof LoginForm> = {
    title: 'Modules/LoginForm',
    component: LoginForm,
};

export default meta;
type Story = StoryObj<typeof LoginForm>;

export const ValidationFailure: Story = {
    play: async ({ canvasElement }: { canvasElement: HTMLElement }) => {
        const canvas = within(canvasElement);
        const submitBtn = canvas.getByRole('button', { name: /entrar/i });

        // Clic sin llenar datos
        await userEvent.click(submitBtn);

        // Verificar mensajes de error
        await expect(canvas.getByText(/email es requerido/i)).toBeInTheDocument();
        await expect(canvas.getByText(/password es requerido/i)).toBeInTheDocument();
    },
};

export const SuccessfulLogin: Story = {
    play: async ({ canvasElement }: { canvasElement: HTMLElement }) => {
        const canvas = within(canvasElement);

        // Llenar campos
        await userEvent.type(canvas.getByLabelText(/email/i), 'admin@test.com');
        await userEvent.type(canvas.getByLabelText(/password/i), '123456');

        // Click submit
        await userEvent.click(canvas.getByRole('button', { name: /entrar/i }));

        // Verificar redirección o mensaje de éxito
        await expect(canvas.getByText(/bienvenido de nuevo/i)).toBeInTheDocument();
    },
};
