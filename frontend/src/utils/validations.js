// Validación de campo requerido
export const required = val => (val !== null && val !== '') || 'Este campo es obligatorio';

// Validación de email
export const email = val => /.+@.+\..+/.test(val) || 'Debe ser un correo válido';

// Validación de cantidad mínima de caracteres
export const minLength = min => val => val.length >= min || `Debe tener al menos ${min} caracteres`;

// Validación de cantidad máxima de caracteres
export const maxLength = max => val => val.length <= max || `Debe tener como máximo ${max} caracteres`;

// Validación de rango de caracteres (cantidad mínima y máxima de caracteres)
export const lengthRange = (min, max) => val => {
    if (val.length < min) {
        return `Debe tener al menos ${min} caracteres`;
    }
    if (val.length > max) {
        return `Debe tener como máximo ${max} caracteres`;
    }
    return true; // Pasa la validación
};

// Validación de un rango de números
export const numberRange = (min, max) => val => (val >= min && val <= max) || `Debe estar entre ${min} y ${max}`;

// Validación de números enteros
export const isInteger = val => Number.isInteger(Number(val)) || 'Debe ser un número entero';

// Validación de números decimales
export const isDecimal = val => !isNaN(val) && val.toString().indexOf('.') !== -1 || 'Debe ser un número decimal';

// Validación de número de teléfono
export const phone = val => /^[0-9]{10}$/.test(val) || 'Debe ser un número de teléfono válido de 10 dígitos';

// Validación de una URL
export const url = val => /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/.test(val) || 'Debe ser una URL válida';

// Validación de que los valores coincidan (por ejemplo, contraseñas)
export const match = otherVal => val => val === otherVal || 'Los valores no coinciden';

// Validación de caracteres alfabéticos solamente
export const alpha = val => /^[a-zA-Z]+$/.test(val) || 'Solo se permiten caracteres alfabéticos';

// Validación de caracteres alfanuméricos
export const alphaNumeric = val => /^[a-zA-Z0-9]+$/.test(val) || 'Solo se permiten caracteres alfanuméricos';

// Validación de caracteres especiales
export const specialChars = val => /[^a-zA-Z0-9]/.test(val) || 'Debe contener caracteres especiales';
