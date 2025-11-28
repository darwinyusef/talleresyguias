// 1. Operaciones Matemáticas Básicas
function sumar(a, b) {
    return a + b;
}

function restar(a, b) {
    return a - b;
}

function multiplicar(a, b) {
    return a * b;
}

function dividir(a, b) {
    if (b === 0) {
        throw new Error("No se puede dividir por cero");
    }
    return a / b;
}

// 2. Manipulación de Strings
function esPalindromo(str) {
    if (!str) return false;
    const limpio = str.toLowerCase().replace(/[\W_]/g, '');
    return limpio === limpio.split('').reverse().join('');
}

function contarVocales(str) {
    if (typeof str !== 'string') return 0;
    const matches = str.match(/[aeiouáéíóú]/gi);
    return matches ? matches.length : 0;
}

// 3. Arrays
function filtrarPares(numeros) {
    if (!Array.isArray(numeros)) return [];
    return numeros.filter(n => n % 2 === 0);
}

function obtenerMaximo(numeros) {
    if (!Array.isArray(numeros) || numeros.length === 0) {
        throw new Error("El array no puede estar vacío");
    }
    return Math.max(...numeros);
}

// 4. Asincronía (Simulación)
function obtenerUsuario(id) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (id === 1) {
                resolve({ id: 1, nombre: "Usuario Prueba", email: "test@example.com" });
            } else {
                reject(new Error("Usuario no encontrado"));
            }
        }, 100); // Simula delay
    });
}

// 5. Integración (Simulación de Servicios)
// Esta función depende de 'obtenerUsuario' (definida arriba), creando un escenario de integración.
function obtenerPerfilCompleto(id) {
    return obtenerUsuario(id).then(usuario => {
        // Simula lógica de negocio adicional sobre el dato obtenido
        return {
            ...usuario,
            nombreCompleto: `${usuario.nombre} (Verificado)`,
            fechaRegistro: new Date().toISOString()
        };
    });
}

// 6. A/B Testing (Lógica de Negocio)
// Simula una función que devuelve diferente contenido según la variante del experimento.
function obtenerTextoBoton(variante) {
    if (variante === 'A') {
        return "Comprar ahora";
    } else if (variante === 'B') {
        return "Añadir al carrito";
    }
    return "Ver producto"; // Control
}

// 7. Flujo Completo (Simulación de Estado para E2E)
// Una clase que mantiene estado, ideal para probar flujos de múltiples pasos (setup -> action -> verification).
class CarritoCompra {
    constructor() {
        this.items = [];
        this.total = 0;
    }

    agregarProducto(nombre, precio) {
        if (!nombre || precio <= 0) {
            throw new Error("Producto inválido");
        }
        this.items.push({ nombre, precio });
        this.total += precio;
    }

    eliminarProducto(nombre) {
        const index = this.items.findIndex(i => i.nombre === nombre);
        if (index !== -1) {
            this.total -= this.items[index].precio;
            this.items.splice(index, 1);
        }
    }

    checkout() {
        if (this.items.length === 0) {
            throw new Error("El carrito está vacío");
        }
        return {
            status: "completado",
            itemsProcesados: this.items.length,
            totalPagado: this.total
        };
    }
}

// Exportar para poder testear (CommonJS o ES Modules según configuración, usaremos CommonJS por compatibilidad básica)
module.exports = {
    sumar,
    restar,
    multiplicar,
    dividir,
    esPalindromo,
    contarVocales,
    filtrarPares,
    obtenerMaximo,
    obtenerUsuario,
    obtenerPerfilCompleto,
    obtenerTextoBoton,
    CarritoCompra
};
