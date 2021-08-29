<template>
  <v-data-table
    :headers="headers"
    :items="friends"
    sort-by="calories"
    class="elevation-1"
    :hide-default-footer="true"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Friends</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
          <template >
            <v-btn color="primary" @click="openForm()" dark class="mb-2" v-on="on">
              Add
            </v-btn>
          </template>
        <v-dialog v-model="dialog" max-width="500px" v-on="on">
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="9" md="9">
                    <v-text-field
                      v-model="friend.name"
                      label="Name"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" sm="12" md="12">
                    <v-text-field
                      v-model="friend.email"
                      label="email"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" text @click="save"> Save </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
  </v-data-table>
</template>

<script>

import axios from 'axios';

export default {
  data: () => ({
    dialog: false,
    headers: [
      { text: 'Name', value: 'name' },
      { text: 'email', value: 'email' },
    ],
    friends: [],
    friend: {
      name: '',
      email: '',
    },
  }),
  computed: {
    formTitle() {
      return 'New Friend';
    },
  },
  methods: {
    initialize() {
      this.friends = [
        {
          name: 'Daniel',
          email: 'd@gmail.com',
        },
        {
          name: 'Leandro',
          email: 'l@gmail.com',
        },
      ];
    },
    openForm() {
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
    save() {
      this.friends.push(this.friend);
      this.close();

      const data = {
        email: this.friend.email,
        name: this.friend.name,
      };
      const path = 'user/invite';
      const headers = { 'Content-Type': 'application/json' };
      axios
        .post(path, data, { headers })
        .then(() => {})
        .catch(() => {});
      this.friend = { name: '', email: '' };
    },
    getFriends() {
      const path = 'user/list_friends';
      axios
        .get(path)
        .then((res) => {
          this.friends = res.data;
        });
    },
  },
  created() {
    this.getFriends();
  },
};
</script>
