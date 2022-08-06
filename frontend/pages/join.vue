<template>
  <div class="main-container">
    <p class="text-center">
      Идентификатор лобби
    </p>
    <input v-model="lobby_id" class="inp tracking-widest" maxlength="8" type="text">
    <button v-cursor-btn class="btn" @click="join_lobby">
      Присоединиться
    </button>
    <button v-cursor-btn class="btn" @click="$router.push('/')">
      ←
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

interface JoinResult {
  success: boolean
}

export default Vue.extend({
  name: 'JoinPage',
  data () {
    return {
      lobby_id: ''
    }
  },
  mounted () {
    this.$socket.on('lobby_probe', this.lobby_probe)
  },
  beforeDestroy () {
    this.$socket.offAny(this.lobby_probe)
  },
  methods: {
    join_lobby () {
      this.$game.lobby_manager.join_lobby(this.lobby_id)
    },
    lobby_probe (resp: JoinResult) {
      if (resp.success) {
        this.$router.push('/lobby')
      } else {
        this.lobby_id = ''
      }
    }
  }
})
</script>

<style scoped>

</style>
