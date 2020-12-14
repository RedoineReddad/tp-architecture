import Vue from 'vue';
import VueRouter from 'vue-router';
import Tickets from '../components/Tickets.vue';
import Login from '../components/Login.vue';
import Booked from '../components/Booked.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/tickets/available',
    name: 'Tickets',
    component: Tickets,
  },
  {
    path: '/tickets/booked',
    name: 'Booked',
    component: Booked,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
