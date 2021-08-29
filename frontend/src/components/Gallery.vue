<template>
    <v-container>
    <v-pagination
      v-model="page"
      :length="totalPages"
     @input="handlePageChange"
    ></v-pagination>
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
import authHeader from '../services/auth-header';
import PhotoListItem from './PhotoListItem.vue';
import PhotoUploader from './PhotoUploader.vue';

export default {
  components: { PhotoListItem, PhotoUploader },
  name: 'Gallery',

  data() {
    return {
      photos: [],
      file: null,
      totalPages: 0,
      page: 1,
      currentPage: 1,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  methods: {
    getPhotos() {
      const path = `photos/list_page/${this.page}`;
      // const path = 'photos/list/all';
      axios
        .get(path, { headers: authHeader() })
        .then((res) => {
          this.photos = JSON.parse(res.data.photos);
          this.totalPages = res.data.totalPages;
          this.currentPage = res.data.currentPage;
        });
    },
    handlePageChange(value) {
      this.currentPage = value;
      this.getPhotos();
    },
  },
  created() {
    this.getPhotos();
  },
};
</script>
