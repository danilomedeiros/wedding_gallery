import Vue from 'vue';
import VueRouter from 'vue-router';
import Gallery from '../components/Gallery.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Friends from '../views/Friends.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/gallery',
    name: 'Gallery',
    component: Gallery,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/',
    name: 'Gallery',
    component: Gallery,
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/register',
    component: Register,
  },
  {
    path: '/friends',
    component: Friends,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
