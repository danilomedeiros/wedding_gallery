<template>
  <v-card hover flat>
      <form>
        <v-file-input
          show-size
          accept="image/png, image/jpeg, image/bmp"
          placeholder="Click here to select your file"
          label="File name"
          prepend-icon="mdi-camera"
          v-model="file"
          >
        </v-file-input>
        <div class="mt-3">{{ file ? 'Selected file:'+file.name : "" }}</div>
        <v-btn
          v-if="file"
          depressed
          color="primary"
          @click="onSubmit"
          @submit.prevent="onSubmit" @reset="onReset"
          >
          Upload
        </v-btn>
      </form>
  </v-card>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  methods: {
    selectPhoto() {
    },
    addPhoto(formData) {
      const path = 'photos/add';
      const headers = { 'Content-Type': 'application/json' };
      axios
        .post(path, formData, { headers })
        .then(() => {
          // this.getPhotos();
        })
        .catch(() => {
          // this.getPhotos();
        });
    },
    initForm() {
      this.file = null;
    },
    onSubmit(evt) {
      evt.preventDefault();
      const formData = new FormData();
      let userId = 0;
      if (this.currentUser) {
        userId = this.currentUser.profile._id;
      }
      formData.append('file', this.file);
      formData.append('user_id', userId);
      this.addPhoto(formData);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPhotoModal.hide();
      this.initForm();
    },
  },
};
</script>
