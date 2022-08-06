<template>
  <div class="main-container">
    <p>Идентификатор лобби: <span class="font-bold select-all">{{ $game.lobby_manager.lobby.id }}</span></p>
    <div class="p-4 main-container border rounded-2xl">
      <p class="text-center text-2xl">
        Игроки (<span class="font-bold">{{ $game.lobby_manager.lobby.users.length }}</span> чел.)
      </p>
      <div v-for="player in $game.lobby_manager.lobby.users" :key="player.user.id">
        <div class="flex items-center space-x-10">
          <user-avatar :user="player.user" />
          <p class="text-xl font-bold">
            {{ player.user.name }} {{ player.ready ? '🔥' : '⚡' }}
          </p>
        </div>
      </div>
    </div>
    <transition name="todo">
      <button
        v-if="$game.lobby_manager.lobby.users.length > 1"
        v-cursor-btn
        class="btn"
        @click="$game.lobby_manager.ready_switch()"
      >
        {{ $game.lobby_manager.ready ? 'Я не готов' : 'Я готов' }}
      </button>
    </transition>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'LobbyPage',
  data () {
    return {}
  },
  mounted () {
    this.$socket.once('game_started', args => this.game_started(args))
  },
  methods: {
    game_started (_: any) {
      this.$router.push('/game')
    }
  }
})
</script>

<style scoped>

</style>
