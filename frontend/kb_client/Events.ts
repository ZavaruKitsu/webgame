import { Session } from '~/kb_client/models/Session'
import { GameLobby } from '~/kb_client/models/Lobby'
import { Message } from '~/kb_client/models/Message'

export interface LobbyUpdated extends GameLobby {

}

export interface GameUpdated extends Session {

}

export interface GameNewMessage extends Message {

}
