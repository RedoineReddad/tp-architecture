<template>
  <div id="login" class="container">
    <h1>Login</h1>
    <form method="post">
      <input type="text" required="required" placeholder="email" v-model="loginForm.email">
      <button class="btn btn-primary" type="button" v-on:click="onSubmit()">Accès au vols</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loginForm: {
        email: '',
      },
    };
  },
  methods: {
    SignIn(payload) {
      const path = 'http://localhost:5000/login';
      let dest = 'http://localhost:5000/tickets/booked?uid=';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data[0].id);
          dest += res.data[0].id;
          // console.log(payload.email);
          axios.get(dest);
          // this.$router.replace({ name: 'Tickets' });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit() {
      // console.log('here is the email');
      // console.log(this.loginForm.email);
      const payload = {
        email: this.loginForm.email,
      };
      this.SignIn(payload);
    },
  },
  created() {
  },
};
</script>
