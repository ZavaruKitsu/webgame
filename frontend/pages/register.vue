<template>
  <div class="main-container">
    <validation-observer v-slot="{invalid}" class="main-container">
      <transition>
        <div v-if="error_visible" class="error-box">
          Что-то не так... Проверь все поля!
        </div>
      </transition>
      <validation-provider v-slot="{errors}" class="relative" name="Юзернейм" rules="required">
        <input v-model="form.name" class="inp" placeholder="Юзернейм" type="text">
        <p class="error-msg">
          {{ errors[0] }}
        </p>
      </validation-provider>
      <validation-provider v-slot="{errors}" class="relative" name="Пароль" rules="required">
        <input v-model="form.password" class="inp" placeholder="Пароль" type="password">
        <p class="error-msg">
          {{ errors[0] }}
        </p>
      </validation-provider>
      <validation-provider v-slot="{errors}" class="relative" name="Аватарка" rules="url">
        <input v-model="form.avatar" class="inp" placeholder="Аватарка" type="text">
        <p class="error-msg">
          {{ errors[0] }}
        </p>
      </validation-provider>
      <div class="p-4 flex flex-col space-y-4 text-center items-center justify-center border rounded-2xl">
        <p class="font-bold">
          Превью аватарки
        </p>
        <user-avatar :user="form" />
      </div>
      <button v-cursor-btn :disabled="invalid" class="btn" @click="register_account">
        Зарегистрироваться
      </button>
    </validation-observer>
    <button v-cursor-btn class="btn" @click="$router.push('login')">
      →
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'RegisterPage',
  auth: 'guest',
  data () {
    return {
      form: {
        name: '',
        password: '',
        avatar: ''
      },
      error_visible: false
    }
  },
  methods: {
    async register_account () {
      try {
        const res = await this.$axios.post('/rest/register', this.form)
        if (res.data.success) {
          await this.$auth.loginWith('local', {
            data: {
              name: this.form.name,
              password: this.form.password
            }
          })
        }
      } catch (error) {
        this.form.password = ''
        this.error_visible = true
        setTimeout(() => {
          this.error_visible = false
        }, 2000)
      }
    }
  }
})
</script>

<style scoped>

</style>
