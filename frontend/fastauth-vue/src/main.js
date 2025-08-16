import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

import Home from './components/Home.vue';
import GoogleCallback from './components/GoogleCallback.vue';

const routes = [
    { path: '/', component: Home },
    { path: '/auth/google', component: GoogleCallback }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

createApp(App).use(router).mount('#app');