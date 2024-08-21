// src/boot/pinia.js
import { createPinia } from 'pinia';

export default ({ app }) => {
    const pinia = createPinia();
    app.use(pinia);
};
