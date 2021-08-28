/* eslint no-use-before-define: 0 */ // --> OFF

import axios from 'axios';

/* eslint-disable no-debugger, no-console */
class AuthService {
  login(user) {
    this.a = '';

    const headers = { 'Content-Type': 'application/json' };

    return axios
      .post('api/login', {
        login: user.login,
        password: user.password,
      },
      { headers })
      .then((response) => {
        if (response.data.accessToken) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
      });
  }

  logout() {
    this.a = '';
    localStorage.removeItem('user');
  }

  register(user) {
    this.a = '';
    return axios.post('logout', {
      login: user.login,
      password: user.password,
    });
  }
}

export default new AuthService();

/* eslint no-use-before-define: 2 */ // --> ON
