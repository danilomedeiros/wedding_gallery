<template>
  <v-app id="inspire">
    <notification ref="notification"></notification>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Register</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form @submit.prevent="handleLogin">
                  <v-text-field
                    name="email"
                    label="e-mail"
                    v-model="user.email"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    name="name"
                    label="Name"
                    v-model="user.name"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    name="login"
                    label="Login"
                    v-model="user.login"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    id="password"
                    name="password"
                    label="Password"
                    type="password"
                    v-model="user.password"
                  ></v-text-field>
                  <v-text-field
                    id="password2"
                    name="password2"
                    label="Repeat Password"
                    type="password"
                    v-model="user.password2"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn :disabled="!(user.email && user.name && user.login && user.password && (user.password == user.password2))" @click="handleRegister" color="primary">Register</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>

import axios from 'axios';
import User from '../models/users';
// eslint-disable-next-line no-unused-vars
import Notification from '../components/Notification.vue';

export default {
  name: 'Login',
  components: {
    Notification,
  },
  data() {
    return {
      user: new User('', '', '', '', ''),
      loading: false,
      message: '',
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      // this.$router.push('/profile');
    }
  },
  mounted() {
    this.$root.notification = this.$refs.notification;
  },
  methods: {
    handleRegister(evt) {
      evt.preventDefault();
      this.loading = true;
      console.log(this.user.email);
      console.log(this.user.name);
      console.log(this.user.login);
      console.log(this.user.password);
      if (this.user.email && this.user.name && this.user.login && this.user.password) {
        const data = {
          email: this.user.email,
          name: this.user.name,
          login: this.user.login,
          password: this.user.password,
        };

        const path = '/user/register';
        const headers = { 'Content-Type': 'application/json' };
        axios
          .post(path, data, { headers })
          .then(() => {
            this.$router.push('/login');
          },
          (e) => {
            this.$root.notification.show({ message: e.response.data, color: 'error' });
          });
      }
    },
  },
};
</script>

<style scoped>
label {
  display: block;
  margin-top: 10px;
}

.card-container.card {
  max-width: 350px !important;
  padding: 40px 40px;
}

.card {
  background-color: #f7f7f7;
  padding: 20px 25px 30px;
  margin: 0 auto 25px;
  margin-top: 50px;
  -moz-border-radius: 2px;
  -webkit-border-radius: 2px;
  border-radius: 2px;
  -moz-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
}

.profile-img-card {
  width: 96px;
  height: 96px;
  margin: 0 auto 10px;
  display: block;
  -moz-border-radius: 50%;
  -webkit-border-radius: 50%;
  border-radius: 50%;
}
</style>
