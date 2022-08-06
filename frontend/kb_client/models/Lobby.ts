import { LobbyUser } from '~/kb_client/models/LobbyUser'

export interface GameLobby {
  id: string
  users: LobbyUser[]
}
