import * as React from "react"
import { GameButton } from "@/components/ui/game-button"
import { GameHoverCard, GameHoverCardContent, GameHoverCardTrigger } from "@/components/ui/game-hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof GameButton> {
  uid: string
  skillName: string
  description: string
  damage?: number
  accuracy?: number
  cost?: number
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, damage, accuracy, cost, ...props }, ref) => {
    return (
      <GameHoverCard uid={`${uid}-hover`}>
        <GameHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <GameButton ref={ref} uid={`${uid}-button`} {...props}>
            {skillName}
          </GameButton>
        </GameHoverCardTrigger>
        <GameHoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-xs text-muted-foreground">
              {damage && <div>Damage: {damage}</div>}
              {accuracy && <div>Accuracy: {accuracy}%</div>}
              {cost && <div>Cost: {cost}</div>}
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
