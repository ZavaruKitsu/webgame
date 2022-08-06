<template>
  <div class="w-screen h-screen flex flex-col justify-center items-center">
    <particles id="background-particles" url="/particlesjs-config.json" />
    <div class="w-full backdrop-blur divide-y md:w-1/2 2xl:w-1/4 p-8 py-4 shadow-lg border rounded-2xl">
      <p class="pb-4 font-bold text-xl text-center">
        💸 КБ ПУМ ✈️
      </p>
      <nuxt />
      <div v-if="$auth.loggedIn" class="pt-4">
        <p class="text-center">
          Добро пожаловать, <span class="font-bold">{{ $auth.user.name }} ~</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'DefaultLayout'
})
</script>
