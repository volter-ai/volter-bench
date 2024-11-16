import * as React from "react"
import { Button, ButtonProps } from "@/components/ui/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { withClickable } from "@/lib/withClickable"

interface SkillButtonProps extends ButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, onClick, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <Button
            ref={ref}
            uid={uid}
            onClick={onClick}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.cost && <div>Cost: {stats.cost}</div>}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"
SkillButton = withClickable(SkillButton)

export { SkillButton }
