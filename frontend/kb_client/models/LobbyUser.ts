import { User } from '~/kb_client/models/User'

export interface LobbyUser {
  user: User
  ready: boolean
}
