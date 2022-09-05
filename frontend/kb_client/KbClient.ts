import { io, Socket } from 'socket.io-client'
import { GameNewMessage, GameUpdated, LobbyUpdated } from '~/kb_client/Events'
import { Session } from '~/kb_client/models/Session'
import { GameLobby } from '~/kb_client/models/Lobby'
import { Player } from '~/kb_client/models/Player'
import { Message } from '~/kb_client/models/Message'

export class GameManager {
  session: Session
  messages: Message[]
  private socket: Socket
  private user_id: string

  constructor (socket: Socket, userId: string) {
    this.socket = socket
    this.user_id = userId
    this.session = {
      id: 'none',
      players: [
        {
          user: {
            id: '1',
            avatar: 'https://avatarfiles.alphacoders.com/307/thumb-1920-307713.jpg',
            name: 'ZavaruKitsu',
            wins: 69,
            looses: 0
          },
          money: 10_000,
          workshops: 2,
          ore: 4,
          airships: 2,
          dead: false
        },
        {
          user: {
            id: '2',
            avatar: 'https://avatarfiles.alphacoders.com/302/thumb-1920-302953.png',
            name: 'Hu Tao',
            wins: 69,
            looses: 0
          },
          money: 20_000,
          workshops: 3,
          ore: 1,
          airships: 1,
          dead: false
        }
      ],
      market_state: {
        level: 3,
        total_ore: 2,
        airships_demand: 3,
        minimal_price: 300,
        maximal_price: 4_500
      },
      queue: ['1', '2'],
      ended: false
    }
    this.messages = []

    this.socket.on('game_updated', args => this.game_updated(args))
    this.socket.on('game_new_message', args => this.game_new_message(args))
  }

  get current_player () {
    return this.get_player(this.user_id)
  }

  send_message (text: string) {
    this.socket.emit('game_send_message', { text })
  }

  make_move (move: any) {
    this.socket.emit('game_make_move', move)
  }

  get_player (userId: string): Player {
    for (const player of this.session.players) {
      if (player.user.id === userId) {
        return player
      }
    }

    return {
      user: {
        id: 'SYSTEM',
        avatar: 'https://avatarfiles.alphacoders.com/307/thumb-1920-307195.gif',
        name: 'СИСТЕМА',
        wins: 69,
        looses: 0
      },
      money: 1,
      workshops: 0,
      airships: 0,
      ore: 0,
      dead: false
    }
  }

  private game_updated (args: GameUpdated) {
    this.session = args
  }

  private game_new_message (args: GameNewMessage) {
    this.messages.push(args)
  }
}

export class LobbyManager {
  lobby: GameLobby
  ready: boolean
  private socket: Socket

  constructor (socket: Socket) {
    this.socket = socket
    this.lobby = {
      id: 'none',
      users: []
    }
    this.ready = false

    this.socket.on('lobby_updated', args => this.lobby_updated(args))
  }

  join_lobby (id: string) {
    this.socket.emit('join_lobby', { lobby_id: id })
  }

  ready_switch () {
    this.socket.emit('lobby_user_ready_switch')
    this.ready = !this.ready
  }

  private lobby_updated (args: LobbyUpdated) {
    this.lobby = args
  }
}

export class KbClient {
  token: string
  socket: Socket
  lobby_manager: LobbyManager
  game_manager: GameManager

  constructor (token: string, userId: string) {
    this.token = token ?? ''
    this.socket = io('http://localhost:3001/', { query: { jwt: token } })
    // this.socket = io('https://kb.radolyn.com/', { query: { jwt: token }, path: '/api/socket.io/' })

    this.lobby_manager = new LobbyManager(this.socket)
    this.game_manager = new GameManager(this.socket, userId)
  }
}
