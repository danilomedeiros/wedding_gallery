import axios from 'axios';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';

axios.defaults.baseURL = '';
Vue.config.productionTip = false;
Vue.config.silent = true;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
