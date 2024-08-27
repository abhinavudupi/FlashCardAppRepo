import { createMemoryHistory, createRouter } from 'vue-router';
import Home from '../views/home.vue';
import Dashboard from '../views/dashboard.vue';
import Deckview from '../views/deckview.vue';
import Review from '../views/review.vue';


const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/deckview',
    name: 'deckview',
    component: Deckview,
  },
  {
    path: '/review',
    name: 'review',
    component: Review,
  },
];


const router = createRouter({
  history: createMemoryHistory(),
  routes,
});

export default router;
