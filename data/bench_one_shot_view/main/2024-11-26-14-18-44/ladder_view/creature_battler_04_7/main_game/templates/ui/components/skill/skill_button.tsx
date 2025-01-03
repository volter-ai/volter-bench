import * as React from "react"
import { Button } from "@/components/ui/button"
import { GameHoverCard, GameHoverCardContent, GameHoverCardTrigger } from "@/components/ui/game-hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
  onClick?: () => void
  disabled?: boolean
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, onClick, disabled, ...props }, ref) => {
    return (
      <GameHoverCard uid={`${uid}-hover`}>
        <GameHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            onClick={onClick}
            disabled={disabled}
            className="w-full"
            {...props}
          >
            {name}
          </Button>
        </GameHoverCardTrigger>
        <GameHoverCardContent uid={`${uid}-content`} className="w-72">
          <div className="space-y-2">
            <h4 className="font-medium">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.cost && <div>Cost: {stats.cost}</div>}
            </div>
          </div>
        </GameHoverCardContent>
      </GameHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
