<template>
  <div id="app">
    <!-- <G6Editor mode="edit"></G6Editor> -->
    <router-view />
  </div>
</template>

<script>
import G6Editor from './components/G6Editor'
import ResizeMixin from './mixin/ResizeHandler'
import WebSocket from './mixin/socket'
import { mapGetters } from 'vuex';

export default {
  name: 'app',
  components: { G6Editor },
  mixins: [ResizeMixin, WebSocket],
  computed: {
    ...mapGetters(['token'])
  },
  created() {
    if (this.token) {
      WebSocket.initWebSocket()
    }
    this.$store.dispatch('app/getCategory')
    this.$store.dispatch('app/getNodeList')
  }
}
</script>

<style>
/* html, body {
    overflow: hidden;
    margin: 0;
    font-size: 12px;
} */
html,
body,
#app {
  font-family: sans-serif, Helvetica, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  line-height: 1.5;
  font-size: 15px;
  height: 100%;
  width: 100%;
  margin: 0;
  /* margin-top: 60px; */
}
</style>
