<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <h1>Wedding Gallery</h1>
      </div>

      <v-spacer></v-spacer>
        <div v-if="!currentUser" >
          <v-btn
          to="/login"
          text
          >
          <span class="mr-2">Login</span>
          <v-icon>mdi-open-in-new</v-icon>
          </v-btn>
          <v-btn
          to="/register"
          text
          >
          <span class="mr-2">Register as a guest</span>
          <v-icon>mdi-open-in-new</v-icon>
          </v-btn>
        </div>
        <div v-if="currentUser" >
          <v-btn v-if="currentUser.profile.typee == 'engaged'"
          to=/friends
          text
          >
          <span class="mr-2">Friends</span>
          <v-icon>mdi-open-in-new</v-icon>
          </v-btn>

          <v-btn
          @click.prevent="logOut"
          text
          >
          <span class="mr-2">Logout</span>
          <v-icon>mdi-open-in-new</v-icon>
          </v-btn>
        </div>

    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    //
  }),
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    showAdminBoard() {
      if (this.currentUser && this.currentUser.roles) {
        return this.currentUser.roles.includes('ENGAGED');
      }
      return false;
    },
    showModeratorBoard() {
      if (this.currentUser && this.currentUser.roles) {
        return this.currentUser.roles.includes('FRIEND');
      }
      return false;
    },
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
  },
};
</script>
