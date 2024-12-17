import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  GameCard,
  GameCardContent,
  GameCardDescription,
  GameCardFooter,
  GameCardHeader,
  GameCardTitle,
} from "@/components/ui/game_card"
import { GameProgress } from "@/components/ui/game_progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <GameCard uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <GameCardHeader uid={`${uid}-header`}>
          <GameCardTitle uid={`${uid}-title`}>{name}</GameCardTitle>
          <GameCardDescription uid={`${uid}-description`}>HP: {hp}/{maxHp}</GameCardDescription>
        </GameCardHeader>
        <GameCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </GameCardContent>
        <GameCardFooter uid={`${uid}-footer`}>
          <GameProgress uid={`${uid}-progress`} value={(hp / maxHp) * 100} className="w-full" />
        </GameCardFooter>
      </GameCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
