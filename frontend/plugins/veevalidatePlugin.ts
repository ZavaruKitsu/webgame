import { extend, ValidationObserver, ValidationProvider } from 'vee-validate'
import Vue from 'vue'

Vue.component('ValidationObserver', ValidationObserver)
Vue.component('ValidationProvider', ValidationProvider)

extend('required', {
  validate (value) {
    return {
      required: true,
      valid: !['', null, undefined].includes(value)
    }
  },
  computesRequired: true,
  message: 'Обязательное поле'
})

extend('url', (value) => {
  if (value.match(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)/)) {
    return true
  }

  return 'Неправильная ссылка'
})
