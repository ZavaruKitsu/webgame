import { Player } from '~/kb_client/models/Player'
import { MarketState } from '~/kb_client/models/MarketState'

export interface Session {
  id: string
  players: Player[]
  market_state: MarketState
  queue: string[]
  ended: boolean
}
