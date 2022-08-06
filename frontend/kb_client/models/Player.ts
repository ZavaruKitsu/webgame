import { User } from '~/kb_client/models/User'

export interface Player {
  user: User
  money: number
  workshops: number
  ore: number
  airships: number
  dead: boolean
}
