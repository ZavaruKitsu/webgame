<template>
  <img
    v-cursor-img
    :alt="user.name"
    :class="{'w-8 h-8': size === 'mini', 'w-16 h-16': size === 'small', 'w-24 h-24': size === 'medium'}"
    :src="valid ? user.avatar : 'https://avatarfiles.alphacoders.com/305/305492.jpg'"
    class="rounded-full"
  >
</template>

<script lang="ts">
import Vue from 'vue'
import { User } from '~/kb_client/models/User'

export default Vue.extend({
  name: 'UserAvatar',
  props: {
    user: {
      type: Object as () => User,
      required: true
    },
    size: {
      type: String,
      default: 'small'
    }
  },
  data () {
    return {
      valid: true
    }
  },
  watch: {
    user: {
      immediate: true,
      deep: true,
      async handler () {
        await this.validateImage()
      }
    }
  },
  async mounted () {
    await this.validateImage()
  },
  methods: {
    async validateImage () {
      if (!this.user.avatar) {
        this.valid = false
        return
      }

      try {
        const res = await this.$axios.get(this.user.avatar, { progress: false })
        this.valid = res.status === 200

        return
      } catch (err: any) {
        this.valid = err.message.includes('Network Error')
      }
    }
  }
})
</script>
