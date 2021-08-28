import AuthService from '../services/auth.services';
// manager states

const user = JSON.parse(localStorage.getItem('user'));

const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit }, user_) {
      return AuthService.login(user_).then(
        (user__) => {
          commit('loginSuccess', user__);
          return Promise.resolve(user__);
        },
        (error) => {
          commit('loginFailure');
          return Promise.reject(error);
        },
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    register({ commit }, user_) {
      return AuthService.register(user_).then(
        (response) => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        (error) => {
          commit('registerFailure');
          return Promise.reject(error);
        },
      );
    },
  },
  mutations: {
    loginSuccess(state, u) {
      state.status.loggedIn = true;
      state.user = u;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },
  },
};

export default auth;
