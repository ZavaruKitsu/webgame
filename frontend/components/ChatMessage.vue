<template>
  <div class="p-4 bg-poetry-200 flex flex-col w-full">
    <div class="flex flex-row items-center space-x-4">
      <user-avatar :user="player.user" size="mini" />
      <div class="w-full flex flex-row justify-between font-bold">
        <p>{{ player.user.name }}</p>
        <p>{{ message_date }}</p>
      </div>
    </div>
    <p class="pt-2 break-words">
      {{ message.text }}
    </p>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Message } from '~/kb_client/models/Message'

export default Vue.extend({
  name: 'ChatMessage',
  props: {
    message: {
      type: Object as () => Message,
      required: true
    }
  },
  computed: {
    player () {
      return this.$game.game_manager.get_player(this.message.user_id)
    },
    message_date () {
      return new Date(this.message.date).toLocaleString('ru-RU', {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
      })
    }
  }
})
</script>

<style scoped>

</style>
