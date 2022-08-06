<template>
  <div class="flex flex-row">
    <!-- CHAT -->
    <div class="w-1/5 h-screen border-r flex flex-col">
      <div class="shrink-0 h-24 p-4 bg-poetry-600 flex justify-center items-center">
        <p
          class="text-center text-white uppercase text-2xl"
        >
          Чат
        </p>
      </div>
      <div
        class="h-full overflow-y-scroll scrollbar scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-poetry-600 divide-y"
      >
        <chat-message v-for="(message, i) in $game.game_manager.messages" :key="i" :ref="i" :message="message" />
      </div>
      <div class="relative">
        <input
          v-model="chatMessage"
          class="pl-12 p-4 w-full border-y outline-none"
          type="text"
          @keydown.enter="send_message"
        >
        <user-avatar
          :user="$game.game_manager.current_player.user"
          class="absolute left-2 bottom-3"
          size="mini"
        />
      </div>
    </div>
    <!-- GAME -->
    <div class="w-4/5 h-screen flex flex-col">
      <!-- QUEUE -->
      <div class="h-24 p-4 border-b flex flex-row space-x-4">
        <user-avatar
          v-for="id in $game.game_manager.session.queue"
          :key="id"
          :user="$game.game_manager.get_player(id).user"
        />
      </div>
      <div class="h-full grid grid-cols-2">
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Статистика</p>
            <select v-model="selectedPlayer" class="w-auto" name="stats_player">
              <option v-for="player in $game.game_manager.session.players" :key="player.user.id" :value="player">
                {{ player.user.name }}
                {{ player.dead ? ' (банкрот)' : '' }}
              </option>
            </select>
            <img v-if="hideModal" alt="" src="~/assets/images/eye.svg" width="24" @click="hideModal = false">
          </div>
          <div class="mt-16 p-4 flex justify-center">
            <user-avatar :user="selectedPlayer.user" size="medium" />
          </div>
          <div class="flex justify-center">
            <div class="flex flex-col">
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/money.svg" width="24">
                <p>
                  <span class="font-bold">Баланс:</span> {{ selectedPlayer.money }} ₽
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/workshop.svg" width="24">
                <p><span class="font-bold">Мастерских:</span> {{ selectedPlayer.workshops }} шт.</p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/ore.svg" width="24">
                <p><span class="font-bold">Руды:</span> {{ selectedPlayer.ore }} шт.</p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/airship.svg" width="24">
                <p><span class="font-bold">Самолётов:</span> {{ selectedPlayer.airships }} шт.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Ситуация на рынке</p>
          </div>
          <div class="mt-40 flex justify-center">
            <div class="flex flex-col">
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/level.svg" width="24">
                <p><span class="font-bold">Уровень:</span> {{ $game.game_manager.session.market_state.level }} ★</p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/ore.svg" width="24">
                <p>
                  <span class="font-bold">Доступно руды:</span> {{ $game.game_manager.session.market_state.total_ore }}
                  шт.
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/airship.svg" width="24">
                <p>
                  <span class="font-bold">Спрос на самолёты:</span>
                  {{ $game.game_manager.session.market_state.airships_demand }} шт.
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/buy.svg" width="24">
                <p>
                  <span class="font-bold">Мин. цена покупки руды:</span>
                  {{ $game.game_manager.session.market_state.minimal_price }} ₽
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/sell.svg" width="24">
                <p>
                  <span class="font-bold">Макс. цена продажи самолётов:</span>
                  {{ $game.game_manager.session.market_state.maximal_price }} ₽
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- PLAYER MOVE MODAL -->
        <div :class="{'hidden': !modalShown}" class="w-full h-full fixed z-10 overflow-auto bg-black/40">
          <div class="mt-[10%] w-4/5 bg-white">
            <div class="w-full p-8 flex flex-col space-y-4 text-2xl justify-center items-center">
              <div class="flex flex-row space-x-4">
                <p class="uppercase font-bold">
                  Твой ход!
                </p>
                <img v-if="!hideModal" alt="" src="~/assets/images/eye.svg" width="24" @click="hideModal = true">
              </div>
              <div class="w-2/5 flex flex-col space-y-4">
                <div class="flex flex-row space-x-4 justify-between">
                  <p class="w-24">
                    Купить
                  </p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model.number="move.ore_request_amount"
                      :max="$game.game_manager.session.market_state.total_ore"
                      class="inp2"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/ore.svg" width="24">
                  </div>
                  <p>за</p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model.number="move.ore_request_price"
                      :min="$game.game_manager.session.market_state.minimal_price"
                      class="inp2"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/money.svg" width="24">
                  </div>
                </div>
                <div class="flex flex-row space-x-4 justify-between">
                  <p class="w-24">
                    Продать
                  </p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model.number="move.sell_request_amount"
                      :max="$game.game_manager.current_player.airships"
                      class="inp2"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/airship.svg" width="24">
                  </div>
                  <p>за</p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model.number="move.sell_request_price"
                      :max="$game.game_manager.session.market_state.maximal_price"
                      class="inp2"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/money.svg" width="24">
                  </div>
                </div>
                <div class="flex flex-row space-x-4 justify-between">
                  <p class="w-24">
                    Изготовить
                  </p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model.number="move.airships_amount"
                      :max="canBuild"
                      class="inp2"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/airship.svg" width="24">
                  </div>
                </div>
                <div class="flex flex-row space-x-4 justify-between items-center">
                  <div class="flex flex-row space-x-2">
                    <p>Построить новый цех</p>
                    <img alt="" src="~/assets/images/workshop.svg" width="24">
                  </div>
                  <input v-model="move.build_workshop" type="checkbox">
                </div>
                <button v-cursor-btn class="uppercase btn2" :disabled="continueDisabled" @click="make_move">
                  Готово
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Player } from '~/kb_client/models/Player'

export default Vue.extend({
  name: 'GamePage',
  layout: 'game',
  data () {
    // @ts-ignore
    const selectedPlayer: Player = this.$game.game_manager.current_player

    return {
      selectedPlayer,
      chatMessage: '',
      move: {
        ore_request_amount: 0,
        ore_request_price: 0,
        airships_amount: 0,
        sell_request_amount: 0,
        sell_request_price: 0,
        build_workshop: false
      },
      hideModal: false,
      continueDisabled: false
    }
  },
  computed: {
    modalShown () {
      // @ts-ignore
      return !this.$game.game_manager.session.ended && this.$game.game_manager.session?.queue[0] === this.$auth.user?.id && !this.hideModal
    },
    canBuild () {
      const player = this.$game.game_manager.current_player
      return player.workshops > player.ore ? player.ore : player.workshops
    }
  },
  mounted () {
    const cursor = document.getElementById('cursor-dot')
    cursor!.classList.add('cursor-dot-blacked')

    const circle = document.getElementById('cursor-circle')
    circle!.classList.add('cursor-circle-blacked')

    this.$socket.on('game_new_message', () => {
      this.$nextTick(() => {
        // @ts-ignore
        const msg = this.$refs[this.$game.game_manager.messages.length - 1][0] as Vue
        msg.$el.scrollIntoView({ behavior: 'smooth' })
      })
    })
    this.$socket.on('game_updated', () => {
      this.continueDisabled = false
      const current = this.selectedPlayer

      this.$nextTick(() => {
        for (const player of this.$game.game_manager.session.players) {
          if (player.user.id === current.user.id) {
            this.selectedPlayer = player
            return
          }
        }

        // видимо чел дал по съ***** из игры
        this.selectedPlayer = this.$game.game_manager.session.players[0]
      })
    })
  },
  beforeDestroy () {
    const cursor = document.getElementById('cursor-dot')
    cursor!.classList.remove('cursor-dot-blacked')

    const circle = document.getElementById('cursor-circle')
    circle!.classList.remove('cursor-circle-blacked')
  },
  methods: {
    send_message () {
      const msg = this.chatMessage.trim()

      if (msg && msg.length > 0) {
        this.$game.game_manager.send_message(msg)
        this.chatMessage = ''
      }
    },
    make_move () {
      this.continueDisabled = true
      this.$game.game_manager.make_move(this.move)

      this.move = {
        ore_request_amount: 0,
        ore_request_price: 0,
        airships_amount: 0,
        sell_request_amount: 0,
        sell_request_price: 0,
        build_workshop: false
      }
    }
  }
})
</script>

<style scoped>
.card {
  @apply m-8 p-8;
  @apply bg-poetry-300 shadow-lg;
  @apply text-2xl;
}

select {
  @apply outline-none;
  @apply px-2 rounded-2xl;
}

.inp2 {
  @apply w-24 px-2 border border-black rounded-2xl outline-none;
}

.btn2 {
  @apply p-4 w-full border border-black rounded-2xl;
  @apply transition duration-200;
  @apply hover:bg-gray-50;
}

.btn2:disabled {
  @apply bg-gray-200;
}
</style>
