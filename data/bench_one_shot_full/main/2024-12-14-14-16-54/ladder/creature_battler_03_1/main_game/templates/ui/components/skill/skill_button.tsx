import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  GameHoverCard,
  GameHoverCardContent,
  GameHoverCardTrigger,
} from "@/components/ui/hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  skillName: string
  description: string
  damage?: number
  accuracy?: number
  cost?: number
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, damage, accuracy, cost, className, ...props }, ref) => {
    return (
      <GameHoverCard uid={`${uid}-hover`}>
        <GameHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {skillName}
          </Button>
        </GameHoverCardTrigger>
        <GameHoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="flex gap-4 text-sm">
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
