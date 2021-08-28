<template>
    <v-container>
      <v-layout v-if="currentUser" row wrap>
          <v-flex xs12 sm12 lg12 pa-2>
            <photo-uploader/>
        </v-flex>
      </v-layout>
    <v-layout row wrap>
    </v-layout>
      <v-layout row wrap>
        <v-flex xs12 sm6 lg4 pa-2 v-for="(photo, index) in photos" :key="index">
          <photo-list-item :photo="photo"/>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import axios from 'axios';
import PhotoListItem from './PhotoListItem.vue';
import PhotoUploader from './PhotoUploader.vue';

export default {
  components: { PhotoListItem, PhotoUploader },
  name: 'Gallery',

  data() {
    return {
      photos: [],
      file: null,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  methods: {
    getPhotos() {
      const path = 'photos/list/all';
      axios
        .get(path)
        .then((res) => {
          this.photos = res.data;
        });
      //  .catch((error) => {
      //    // eslint-disable-next-line
      //  });
    },
    addPhoto(formData) {
      const path = 'photos/add';
      const headers = { 'Content-Type': 'application/json' };
      axios
        .post(path, formData, { headers })
        .then(() => {
          this.getPhotos();
        });
      //  .catch((error) => {
      //    // eslint-disable-next-line
      //  });
    },
    initForm() {
      this.file = null;
    },
    onSubmit(evt) {
      evt.preventDefault();
      const formData = new FormData();
      formData.append('file', this.file);
      this.addPhoto(formData);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPhotoModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getPhotos();
  },
};
</script>
