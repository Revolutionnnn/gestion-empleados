export const EMPLOYEE = 1;
export const GUEST = 2;
export const PROVIDER = 3;

export const TYPE_CHOICES = [
    { code: EMPLOYEE, description: 'Empleado' },
    { code: GUEST, description: 'Invitado' },
    { code: PROVIDER, description: 'Proveedor' }
];

export const MEDICAL_QUOTE = 1;
export const CALAMITY = 2;
export const PERSONAL_DILIGENCE = 3;

export const REASON_CHOICES = [
    { code: MEDICAL_QUOTE, description: 'Cita médica' },
    { code: CALAMITY, description: 'Calamidad' },
    { code: PERSONAL_DILIGENCE, description: 'Diligencia personal' }
];
