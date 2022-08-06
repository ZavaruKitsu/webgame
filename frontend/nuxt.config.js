export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'КБ ПУМ',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1'
      },
      {
        hid: 'description',
        name: 'description',
        content: ''
      },
      {
        name: 'format-detection',
        content: 'telephone=no'
      }
    ],
    link: [
      {
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico'
      }
    ]
  },

  ssr: false,

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/css/main'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    {
      src: '~/plugins/gamePlugin',
      mode: 'client'
    },
    '~/plugins/particlesPlugin',
    '~/plugins/veevalidatePlugin',
    '~/plugins/cursorPlugin'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    '@nuxt/postcss8'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  axios: {
    baseURL: process.env.BASE_URL || 'http://localhost:3001'
  },

  auth: {
    strategies: {
      local: {
        property: 'token',
        global: true,
        user: {
          autoFetch: true
        },
        endpoints: {
          login: {
            url: '/rest/login',
            method: 'post'
          },
          user: {
            url: '/rest/me',
            method: 'get'
          }
        }
      }
    },
    redirect: {
      login: '/login',
      home: '/',
      logout: false,
      callback: false
    }
  },

  router: {
    middleware: ['auth'],
    extendRoutes (routes, resolve) {
      routes.push({
        name: 'custom',
        path: '*',
        component: resolve(__dirname, 'pages/index.vue')
      })
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    postcss: {
      plugins: {
        tailwindcss: {},
        autoprefixer: {}
      }
    }
  },
  transpile: [
    'vee-validate/dist/rules'
  ]
}
