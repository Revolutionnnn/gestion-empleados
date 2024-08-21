// stores/user.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        username: null,
        first_name: null,
        last_name: null,
        email: null,
        date_joined: null,
        is_active: null,
    }),
    actions: {
        setProfile(profile) {
            this.username = profile.username;
            this.first_name = profile.first_name;
            this.last_name = profile.last_name;
            this.email = profile.email;
            this.date_joined = profile.date_joined;
            this.is_active = profile.is_active;
        },
        logout() {
            this.username = null;
            this.first_name = null;
            this.last_name = null;
            this.email = null;
            this.date_joined = null;
            this.is_active = null;
        }
    },
    getters: {
        isAuthenticated: (state) => !!state.username,
        getProfile: (state) => ({
            username: state.username,
            first_name: state.first_name,
            last_name: state.last_name,
            email: state.email,
            date_joined: state.date_joined,
            is_active: state.is_active
        }),
    },
});
