<template>
  <div class="main-container">
    <input
      v-model.number="form.months"
      class="inp"
      max="96"
      min="0"
      placeholder="Кол-во месяцев (по умолч. 12)"
      type="number"
    >
    <input
      v-model.number="form.bots"
      class="inp"
      max="4"
      min="0"
      placeholder="Кол-во ботов (по умолч. 0)"
      type="number"
    >
    <button v-cursor-btn class="btn" @click="create_lobby">
      Создать лобби
    </button>
    <button v-cursor-btn class="btn" @click="$router.push('/')">
      ←
    </button>
  </div>
</template>

<script>
export default {
  name: 'CreateGamePage',
  data () {
    return {
      form: {
        months: undefined,
        bots: undefined
      }
    }
  },
  mounted () {
    this.$socket.on('lobby_created', this.lobby_created)
  },
  methods: {
    create_lobby () {
      if (this.form.months === undefined || this.form.months <= 0) {
        this.form.months = 12
      }
      if (this.form.bots === undefined || this.form.bots < 0) {
        this.form.bots = 0
      }

      this.$socket.emit('create_lobby', this.form)
    },
    lobby_created () {
      this.$router.push('lobby')
    }
  }
}
</script>

<style scoped>

</style>
