<template>
  <div class="text-center">
    <v-card hover flat  @click="dialog = true">
      <v-img
        class="white--text"
        height="200px"
        :src="photo.url"
      >
        <template v-slot:placeholder>
          <v-row
            class="fill-height ma-0"
            align="center"
            justify="center"
          >
            <v-progress-circular
              indeterminate
            color="grey lighten-2"
            ></v-progress-circular>
          </v-row>
        </template>
          <v-container fill-height fluid>
          <v-layout fill-height>
            <v-flex xs12 align-end flexbox>
              <h2 class="headline" style="text-shadow: 0px 2px 5px #222;"></h2>
            </v-flex>
          </v-layout>
        </v-container>
      </v-img>
      <!--<v-card-title><div><p class="grey--text">data de publicacao</p></div> </v-card-title>-->
      <!-- pop up-->
    </v-card>
      <v-card-actions>
            <v-switch
              v-if="currentUser && currentUser.profile.typee==='engaged'"
              :label=status_label
              color="accent"
              value=""
              hide-details
              @click="changeStatus"
              v-model="photo_status"
            ></v-switch>
          </v-card-actions>
      <v-dialog fullscreen hide-overlay  transition="dialog-bottom-transition"
        v-model="dialog"
        width="300"
      >
      <v-flex xs12 md8 offset-md2 lg6 offset-lg3>
        <v-card>
          <v-list three-line subheader style="padding-top: 85px;">
            <v-layout
            row justify-center py-2
            class="text-xs-center">
              <v-responsive max-width="600px">
                <v-img
                  :src="photo.url"
                  >
                  <template v-slot:placeholder>
                    <v-row
                      class="fill-height ma-0"
                      align="center"
                      justify="center"
                    >
                      <v-progress-circular
                        indeterminate
                        color="blue"
                      ></v-progress-circular>
                    </v-row>
                  </template>
                </v-img>
              </v-responsive>
            </v-layout>
          </v-list>
          <v-list three-line subheader style="padding-left: 50px;padding-right: 50px;">
            <v-subheader>

              <v-btn v-if="currentUser"  @click.prevent="likeIt()" primary >
                <v-icon v-if="user_liked" color="blue" >mdi-thumb-up</v-icon>
                <v-icon v-else >mdi-thumb-up-outline</v-icon>
                &nbsp;{{total_likes_button}}
              </v-btn>
              <div v-else >
                <v-icon v-if="user_liked" color="blue" >mdi-thumb-up</v-icon>
                <v-icon v-else >mdi-thumb-up-outline</v-icon>
                &nbsp;{{total_likes_button}}
              </div>
            </v-subheader>
          </v-list>
          <div v-if="currentUser"   >
          <v-list three-line subheader style="padding-left: 50px;padding-right: 50px;">
            <v-subheader>Post a comment</v-subheader>

            <v-form ref="commentForm" v-model="validComment" @submit.prevent="postComment()">
              <v-container fluid py-0>
                <v-layout row wrap>
                  <v-flex
                    xs12
                    md6
                  >
                    <v-text-field
                      prepend-icon="mdi-account"
                      v-model="newComment.name"
                      :counter="30"
                      label="your name"
                      required
                    ></v-text-field>
                  </v-flex>
                  <v-flex
                  xs12
                  md6
                  >
                </v-flex>
                <v-flex
                  xs12
                >
                  <v-text-field
                    prepend-icon="mdi-comment-text"
                    v-model="newComment.content"
                    label="comment"
                    :counter="200"
                    required
                  ></v-text-field>
                  <div class="text-xs-right">
                    <v-btn @click.prevent="addComment" type="submit" depressed class="white--text" color="green lighten-1" :disabled="!validComment">Post Comment</v-btn>
                  </div>
                </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </v-list>
          </div>
          <div v-else>
            <v-subheader>log in to post comments</v-subheader>
          </div>
        <v-list three-line subheader style="padding-left: 50px;padding-right: 50px;">
          <v-subheader>{{ comments.length }} Comment(s)</v-subheader>
        <p
          v-if="comments.length <= 0"
        >
          Be the first to leave a comment!
        </p>
        <p></p>
         <template v-for="(comment, i) in comments">
           <v-divider
            :key="i"
            inset
           ></v-divider>

           <v-list-tile
             :key="comment.id"
             avatar
           >
             <v-list-tile-avatar name="avatar">
               <v-icon color="primary" large>mdi-account-circle-outline</v-icon>
             </v-list-tile-avatar>

             <v-list-tile-content>
               <v-list-tile-title v-html="comment.author"></v-list-tile-title>
               :&nbsp;&nbsp;&nbsp;
               <v-list-tile-sub-title v-html="comment.content"></v-list-tile-sub-title>
             </v-list-tile-content>
           </v-list-tile>
         </template>
       </v-list>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="dialog = false"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-dialog>
  </div>
</template>
<script>

import axios from 'axios';

export default {

  data() {
    return {
      dialog: false,
      validComment: false,
      newComment: {
        name: '',
        content: '',
      },
      comments: [],
      total_likes: [0, 0],
      total_likes_button: 0,
      user_liked: false,
      nameRules: [
        (r) => !!r || 'Name is required',
        (r) => r.length <= 0 || 'Name must not be empty',
      ],
      photo_status: false,
      status_label: false,
    };
  },
  props: {
    photo: {
      type: Object,
      required: true,
    },
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },

  },
  methods: {
    addComment() {
      const data = {
        photo_id: this.photo.id,
        author: this.newComment.name,
        content: this.newComment.content,
      };
      const path = 'comments/add';
      const headers = { 'Content-Type': 'application/json' };
      axios
        .post(path, data, { headers })
        .then((e) => {
          this.comments.push(e.data);
          this.newComment.name = null;
          this.newComment.content = null;
          this.getComments();
        })
        .catch(() => {
        });
    },
    getComments() {
      const path = `comments/list/${this.photo.id}`;
      axios
        .get(path)
        .then((res) => {
          this.comments = res.data;
        });
    },
    getLikes() {
      let userId = 0;
      if (this.currentUser) {
        userId = this.currentUser.profile._id;
      }
      const path = `likes/count/${this.photo.id}/${userId}`;
      axios
        .get(path)
        .then((res) => {
          this.total_likes = res.data;
          this.refreshLikeStatus();
        })
        .catch(() => {
        });
    },
    likeIt() {
      let add = 0;
      if (this.user_liked) {
        add = -1;
      } else {
        add = 1;
      }
      this.total_likes[0] = this.total_likes[0] + add;
      this.total_likes[1] = this.total_likes[1] + add;
      this.refreshLikeStatus();
      this.operacao = 'add';
      if (add < 0) {
        this.operacao = 'delete';
      }
      let userId = 0;
      if (this.currentUser) {
        userId = this.currentUser.profile._id;
      }
      const data = {
        photo_id: this.photo.id,
        user_id: userId,
      };
      const path = `likes/${this.operacao}`;
      const headers = { 'Content-Type': 'application/json' };
      axios
        .post(path, data, { headers })
        .then(() => {});
    },
    changeStatus(evt) {
      evt.preventDefault();
      if (this.photo.status === 'on') {
        this.photo.status = 'off';
      } else {
        this.photo.status = 'on';
      }

      const data = {
        photo_id: this.photo.id,
        status: this.photo.status,
      };

      const path = '/photos/changestatus';
      const headers = { 'Content-Type': 'application/json' };
      axios
        .post(path, data, { headers })
        .then(() => {});
      this.updatePhotoStatus();
    },
    refreshLikeStatus() {
      this.total_likes_button = this.total_likes[0];
      this.user_liked = this.total_likes[1] > 0;
    },
    updatePhotoStatus() {
      this.photo_status = (this.photo.status === 'on');
      if (this.photo.status === 'on') {
        this.status_label = 'on';
      } else if (this.photo.status === 'off') {
        this.status_label = 'off';
      } else {
        this.status_label = 'pending';
      }
    },
  },
  created() {
    this.getComments();
    this.getLikes();
    this.updatePhotoStatus();
  },
};
</script>

<style>
</style>
