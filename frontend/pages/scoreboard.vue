<template>
  <div class="main-container">
    <button v-cursor-btn class="btn" @click="main_menu">
      ←
    </button>
    <p class="text-center text-3xl">
      Топ игроков <span class="font-bold">за всё время</span>
    </p>
    <div v-for="(user, i) in users" :key="user.id">
      <div class="flex items-center space-x-10">
        <user-avatar :user="user" />
        <p class="text-xl font-bold">
          {{ i + 1 }}. {{ user.name }} ({{ user.wins + user.looses }}, {{ getWinRate(user).toFixed(2) }}%)
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { User } from '~/kb_client/models/User'

export default Vue.extend({
  name: 'ScoreboardPage',
  async asyncData ({ $axios }) {
    const users = await $axios.$get('/rest/scoreboard')

    return { users }
  },
  data () {
    const users: User[] = []

    return {
      users
    }
  },
  methods: {
    getWinRate (user: User) {
      const rate = (user.wins / (user.wins + user.looses))

      if (isNaN(rate)) {
        return 0
      }

      return rate * 100
    },
    main_menu () {
      this.$router.push('/')
    }
  }
})
</script>

<style scoped>

</style>
