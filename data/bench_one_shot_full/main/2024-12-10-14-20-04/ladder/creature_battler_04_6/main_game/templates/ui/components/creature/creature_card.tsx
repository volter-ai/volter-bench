import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  GameCard,
  GameCardContent,
  GameCardFooter,
  GameCardHeader,
  GameCardTitle,
} from "@/components/ui/game_card"
import { GameProgress } from "@/components/ui/game_progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    const hpPercentage = (currentHp / maxHp) * 100

    return (
      <GameCard uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <GameCardHeader uid={uid}>
          <GameCardTitle uid={uid}>{name}</GameCardTitle>
        </GameCardHeader>
        <GameCardContent uid={uid}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </GameCardContent>
        <GameCardFooter uid={uid} className="flex flex-col gap-2">
          <div className="w-full flex justify-between">
            <span>HP</span>
            <span>{`${currentHp}/${maxHp}`}</span>
          </div>
          <GameProgress uid={uid} value={hpPercentage} className="w-full" />
        </GameCardFooter>
      </GameCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
