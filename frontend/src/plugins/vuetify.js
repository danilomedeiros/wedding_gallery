import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#cc8084',
        secondary: '#e2b7b9',
        accent: '#6eacb7',
        error: '#6eacb7',
        info: '#a1c9d0',
      },
    },
  },
});
