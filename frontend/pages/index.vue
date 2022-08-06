<template>
  <div class="main-container">
    <button v-cursor-btn class="btn" @click="create_lobby">
      Создать лобби
    </button>
    <button v-cursor-btn class="btn" @click="join_lobby">
      Присоединиться к лобби
    </button>
    <button v-cursor-btn class="btn" @click="view_scoreboard">
      Топ игроков
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

interface LobbyCreated {
  lobby_id: string
}

export default Vue.extend({
  name: 'IndexPage',
  mounted () {
    if (this.$game.token === '') {
      location.reload()
    }
  },
  methods: {
    create_lobby () {
      this.$router.push('create')
    },
    join_lobby () {
      this.$router.push('join')
    },
    view_scoreboard () {
      this.$router.push('scoreboard')
    }
  }
})
</script>
